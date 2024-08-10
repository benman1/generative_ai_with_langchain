from config import set_environment

set_environment()

from langchain_community.llms import Replicate

text2image = Replicate(
    model=(
        "stability-ai/stable-diffusion: "
        "27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478"
    ),
    model_kwargs={"image_dimensions": "512x512"}
)
image_url = text2image.invoke(
    "a book cover for a book about creating generative ai applications in Python"
)
print(image_url)


if __name__ == "__main__":
    pass