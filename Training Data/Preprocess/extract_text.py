import argparse
import re
from bs4 import BeautifulSoup

def remove_corrupted_image(text):
    """
    Remove a corrupted image block from the text.
    The pattern looks for a block starting with "GRAPHIC", followed by digits, the image file name,
    the word "begin", and then any characters until "end".
    """
    pattern = r"GRAPHIC\s+\d+\s+g325078g0426062022046a03\.jpg\s+begin.*?end"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return cleaned_text

def is_gibberish(token, diversity_threshold=0.4, alnum_threshold=0.3, min_length=10):
    """
    Determines if a token is likely gibberish.
    If the token is long and the ratio of unique characters (diversity) is low,
    or it contains very few alphanumeric characters, it is considered gibberish.
    """
    if len(token) < min_length:
        return False
    diversity = len(set(token)) / len(token)
    alnum_ratio = sum(c.isalnum() for c in token) / len(token)
    return diversity < diversity_threshold or alnum_ratio < alnum_threshold

def remove_gibberish_tokens(text):
    """
    Splits the text into tokens, filters out tokens that appear to be gibberish,
    and then rejoins the tokens.
    """
    tokens = text.split()
    filtered_tokens = [token for token in tokens if not is_gibberish(token)]
    return ' '.join(filtered_tokens)

def extract_main_text(file_content):
    """
    Parses the file content as HTML, removes script/style elements,
    extracts the text, and applies further cleaning.
    """
    # Use BeautifulSoup to parse the text as HTML.
    soup = BeautifulSoup(file_content, 'html.parser')
    
    # Remove <script> and <style> elements.
    for element in soup(["script", "style"]):
        element.decompose()
    
    # Extract text and normalize whitespace.
    text = soup.get_text(separator=' ')
    clean_text = ' '.join(text.split())
    
    # Remove known corrupted image block.
    clean_text = remove_corrupted_image(clean_text)
    
    # Remove general gibberish tokens.
    clean_text = remove_gibberish_tokens(clean_text)
    
    return clean_text

def main(input_file, output_file):
    # Read the file as text (works regardless of file extension).
    with open(input_file, "r", encoding="utf-8") as f:
        file_content = f.read()
    
    # Process the file content.
    extracted_text = extract_main_text(file_content)
    
    # Write the cleaned text to the output file.
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    print(f"Extraction complete. Clean text saved to {output_file}")

if __name__ == "__main__":
    # Set up command-line arguments.
    parser = argparse.ArgumentParser(
        description="Extract main text from an HTML file (even if saved as .txt), remove corrupted image blocks, and filter out gibberish tokens."
    )
    parser.add_argument("input_file", help="Path to the input text file containing HTML")
    parser.add_argument("output_file", help="Path for the output text file")
    
    args = parser.parse_args()
    main(args.input_file, args.output_file)
