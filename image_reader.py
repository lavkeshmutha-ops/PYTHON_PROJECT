

import re
from PIL import Image


def extract_math_from_image(image_path):

    
    # Open the image with Pillow
    try:
        img = Image.open(image_path)
    except Exception as e:
        return f"Error opening image: {str(e)}"

    # Try pytesseract first (most common OCR tool)
    raw_text = try_pytesseract(img)

    # If pytesseract fails or gives empty result, try easyocr
    if not raw_text or raw_text.strip() == "":
        raw_text = try_easyocr(image_path)

    # If still nothing, return an error message
    if not raw_text or raw_text.strip() == "":
        return ""

    # Clean the extracted text so the solver can understand it
    cleaned = clean_math_text(raw_text)
    return cleaned


def try_pytesseract(img):
    
    try:
        import pytesseract

        # Preprocess: convert to grayscale to improve OCR accuracy
        gray_img = img.convert("L")

        # Use pytesseract to extract text
        # config: treat the image as a single line of text (good for math)
        custom_config = r"--oem 3 --psm 7"
        text = pytesseract.image_to_string(gray_img, config=custom_config)

        return text.strip()

    except ImportError:
        # pytesseract is not installed
        return ""
    except Exception as e:
        # Some other error occurred
        print(f"pytesseract error: {e}")
        return ""


def try_easyocr(image_path):
  
    try:
        import easyocr

        # Initialize the reader for English
        # gpu=False means it runs on CPU (safer for most systems)
        reader = easyocr.Reader(["en"], gpu=False)

        # Read text from the image file path
        results = reader.readtext(image_path, detail=0)

        # Join all detected text pieces together
        text = " ".join(results)
        return text.strip()

    except ImportError:
        # easyocr is not installed
        return ""
    except Exception as e:
        print(f"easyocr error: {e}")
        return ""


def clean_math_text(raw_text):
    
    text = raw_text.strip()

    # Remove newlines and extra spaces
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    # Fix common OCR errors in math:
    text = text.replace("×", "*")    # Multiplication symbol → *
    text = text.replace("÷", "/")    # Division symbol → /
    text = text.replace("²", "**2")  # Superscript 2 → **2
    text = text.replace("³", "**3")  # Superscript 3 → **3
    text = text.replace("√", "sqrt") # Square root symbol
    text = text.replace("π", "pi")   # Pi symbol
    text = text.replace("∫", "integrate(") # Integral symbol (partial fix)

    # Fix common letter-vs-number OCR confusion:
    # OCR often reads 'l' (letter L) as '1' in math context
    # and '0' as 'O' (letter O)
    # We do a conservative replacement here
    text = re.sub(r"\bO\b", "0", text)  # Standalone O → 0

    # Remove stray characters that are not math-related
    # Keep: digits, letters, +, -, *, /, =, ^, (, ), ., space
    text = re.sub(r"[^\w\s\+\-\*/\=\^\(\)\.\,]", "", text)

    # Clean up multiple spaces again after replacements
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_image(img):
    
    from PIL import ImageEnhance, ImageFilter

    # Convert to grayscale
    img = img.convert("L")

    # Increase contrast — helps OCR read math symbols clearly
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # Apply sharpening filter
    img = img.filter(ImageFilter.SHARPEN)

    return img