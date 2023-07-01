import base64

with open("image.jpeg", "rb") as image_file:
    image_data = image_file.read()

base64_image = base64.b64encode(image_data)

base64_image_str = base64_image.decode('utf-8')

print(base64_image_str)


# import base64
# from PIL import Image
# from io import BytesIO

# # Base64-encoded image
# base64_image = "your_base64_encoded_image_here"

# # Decode the image
# decoded_image_data = base64.b64decode(base64_image)

# # Create an image object from the decoded data
# image = Image.open(BytesIO(decoded_image_data))

# # Save the image to a file (optional)
# image.save("decoded_image.jpg")

# # Display the image (optional)
# image.show()