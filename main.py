import os
import openai
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_script(prompt, max_tokens=100):
    """
    Generate a video script using OpenAI's GPT-3.
    
    Args:
        prompt (str): The prompt to generate the script.
        max_tokens (int): The maximum number of tokens to generate.
    
    Returns:
        str: The generated script.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating script: {e}")
        return None

def create_text_clip(text, duration=5, fontsize=50, color='white', bg_color='black'):
    """
    Create a text clip for the video.
    
    Args:
        text (str): The text to display.
        duration (int): Duration of the text clip in seconds.
        fontsize (int): Font size of the text.
        color (str): Text color.
        bg_color (str): Background color.
    
    Returns:
        TextClip: The text clip.
    """
    try:
        return TextClip(text, fontsize=fontsize, color=color, bg_color=bg_color, size=(1280, 720)).set_duration(duration)
    except Exception as e:
        print(f"Error creating text clip: {e}")
        return None

def generate_video(script, output_file="output.mp4"):
    """
    Generate a video from the script.
    
    Args:
        script (str): The script to generate the video from.
        output_file (str): The output file name.
    """
    try:
        # Split script into lines
        lines = script.split('\n')
        
        # Create text clips for each line
        text_clips = [create_text_clip(line) for line in lines if line.strip()]
        
        # Concatenate text clips
        final_clip = concatenate_videoclips(text_clips)
        
        # Write the result to a file
        final_clip.write_videofile(output_file, fps=24)
        print(f"Video generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating video: {e}")

def main():
    prompt = "Create a script for a video about the benefits of AI in daily life."
    script = generate_script(prompt)
    if script:
        generate_video(script)

if __name__ == "__main__":
    main()