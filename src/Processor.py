import av
from av.container.input import InputContainer
from av.container.output import OutputContainer


class Processor:
    input_container: InputContainer
    output_container: OutputContainer

    @staticmethod
    def timestamp_to_frame(timestamp, stream):
        fps = stream.average_rate
        time_base = stream.time_base
        start_time = stream.start_time
        frame = (timestamp - start_time) * float(time_base) * float(fps)

        return frame

    def process(self, input_path: str, output_path: str, start: int, end: int):
        self.input_container = av.open(input_path, stream_options=[{"codec": "h264"}])
        self.output_container = av.open(output_path,
                                        mode="w",
                                        options={
                                            "movflags": "empty_moov+omit_tfhd_offset+frag_keyframe+default_base_moof",
                                        })

        input_video_stream = next(s for s in self.input_container.streams if s.type == "video")
        input_audio_stream = next(s for s in self.input_container.streams if s.type == "audio")

        output_video_stream = self.output_container.add_stream(template=input_video_stream)
        output_audio_stream = self.output_container.add_stream(template=input_audio_stream)

        current_frame = None

        frame_length = float(1 / input_video_stream.average_rate)
        frame_number = round(frame_length * start)
        end_frame_number = round(frame_length * end)

        self.input_container.seek(frame_number, any_frame=True, backward=True, stream=input_video_stream)

        for packet in self.input_container.demux(video=0, audio=0):
            frame_number += 1

            if packet.dts is None:
                continue

            if packet.stream.type == "video":
                packet.stream = output_video_stream
                for frame in packet.decode():
                    if current_frame is None:
                        current_frame = Processor.timestamp_to_frame(frame.pts, input_video_stream)
                    else:
                        current_frame += 1

            elif packet.stream.type == "audio":
                packet.stream = output_audio_stream

            self.output_container.mux(packet)

            if frame_number >= end_frame_number:
                break

        self.output_container.close()

        return {
            "frames_processed": frame_number - start,
            "milliseconds_per_frame": frame_length,
            "milliseconds_output": float(1 / input_video_stream.average_rate * (frame_number - start) * 1000)
        }
