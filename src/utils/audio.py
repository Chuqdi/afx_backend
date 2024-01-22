import os
from typing_extensions import deprecated
import aiohttp
import aiofiles
from pydub import AudioSegment


async def fetch_audio_data(session, url):
    async with session.get(url) as response:
        return await response.read()


# FFMPEG setup on windows -> https://www.youtube.com/watch?v=yqFplTt29A8
@deprecated(
    "`blend_audio_from_urls` is now deprecated as these operations will be handled from the client"
)
async def blend_audio_from_urls(
    actual_audio_url, background_audio_url, background_volume=10
):
    async with aiohttp.ClientSession() as session:
        # Fetch audio data from URLs asynchronously
        actual_audio_data = await fetch_audio_data(session, actual_audio_url)
        background_audio_data = await fetch_audio_data(session, background_audio_url)

        # Create temporary files for audio data
        actual_temp_file = "actual_temp.mp3"
        background_temp_file = "background_temp.mp3"
        output_file = "output.mp3"

        try:
            async with aiofiles.open(actual_temp_file, "wb") as actual_file:
                await actual_file.write(actual_audio_data)

            async with aiofiles.open(background_temp_file, "wb") as background_file:
                await background_file.write(background_audio_data)

            # Create AudioSegments from temporary files
            actual_audio = AudioSegment.from_file(actual_temp_file, format="mp3")
            background_audio = AudioSegment.from_file(
                background_temp_file, format="mp3"
            )

            # Adjust the duration of the actual audio to match the background audio
            actual_audio = actual_audio[: len(background_audio)]

            # Reduce the volume of the background audio
            reduced_background_audio = background_audio - background_volume

            # Blend the two audio tracks
            blended_audio = actual_audio.overlay(reduced_background_audio)

            # TODO: Potentially save this blended audio in S3

            # Export the final result
            blended_audio.export(output_file, format="mp3")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Cleanup: Remove temporary files
            try:
                os.remove(actual_temp_file)
            except Exception as e:
                print(f"Error removing {actual_temp_file}: {e}")

            try:
                os.remove(background_temp_file)
            except Exception as e:
                print(f"Error removing {background_temp_file}: {e}")
