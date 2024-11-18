from unstructured.partition.pdf import partition_pdf
import os
from dotenv import load_dotenv
import base64
from IPython.display import Image, display
import nltk

try:
    nltk.data.find('tokenizers')
except LookupError:
    nltk.download('all')

load_dotenv()

output_path = "./content/"
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print(f"Created directory: {output_path}")

source_directory = os.getenv('DOCS_DIR')
file_path = source_directory + 'China.pdf'


# Get the images from the CompositeElement objects
def get_images_base64(chunks):
    images_b64 = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            chunk_els = chunk.metadata.orig_elements
            for el in chunk_els:
                if "Image" in str(type(el)):
                    images_b64.append(el.metadata.image_base64)
    return images_b64


def display_base64_image(base64_code):
    # Decode the base64 string to binary
    image_data = base64.b64decode(base64_code)
    # Display the image
    display(Image(data=image_data))


def save_base64_image(base64_code, file_path):
    # Decode the base64 string to binary
    image_data = base64.b64decode(base64_code)
    # Write the binary data to a file
    with open(file_path, 'wb') as file:
        file.write(image_data)
    print(f"Image saved to {file_path}")


# Reference: https://docs.unstructured.io/open-source/core-functionality/chunking
chunks = partition_pdf(
    filename=file_path,
    infer_table_structure=True,  # extract tables
    strategy="hi_res",  # mandatory to infer tables

    extract_image_block_types=["Image"],  # Add 'Table' to list to extract image of tables
    # image_output_dir_path=output_path,   # if None, images and tables will saved in base64

    extract_image_block_to_payload=True,  # if true, will extract base64 for API usage

    chunking_strategy="by_title",  # or 'basic'
    max_characters=10000,  # defaults to 500
    combine_text_under_n_chars=2000,  # defaults to 0
    new_after_n_chars=6000,

    # extract_images_in_pdf=True,          # deprecated
)

# We get 2 types of elements from the partition_pdf function
set([str(type(el)) for el in chunks])

# Each CompositeElement containes a bunch of related elements.
# This makes it easy to use these elements together in a RAG pipeline.
print(chunks[3].metadata.orig_elements)

# This is what an extracted image looks like.
# It contains the base64 representation only because we set the param extract_image_block_to_payload=True

elements = chunks[3].metadata.orig_elements
chunk_images = [el for el in elements if 'Image' in str(type(el))]
print(chunk_images[0].to_dict())

# separate tables from texts
tables = []
texts = []

for chunk in chunks:
    if "Table" in str(type(chunk)):
        tables.append(chunk)

    if "CompositeElement" in str(type((chunk))):
        texts.append(chunk)

images = get_images_base64(chunks)

for index, image in enumerate(images):
    save_base64_image(image, os.path.join(output_path, f"image_{index}.png"))
