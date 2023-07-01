from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from hackapp.models import Questions
import openai
from PIL import Image
from io import BytesIO
import base64
from samsunghack.settings import MEDIA_ROOT
import os
from django.http import JsonResponse

openai.api_key = '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'

@api_view(['GET'])
def users(request):
    serializer = RegistrationSerializer(data=request.data)
    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
        })
    return Response(user_data)

@api_view(['POST'])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "Registration successful.", "user_id": user.id})
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({"message": "Login successful."})
    else:
        return Response({"message": "Invalid username or password."}, status=401)


@api_view(['POST'])
def image(request):
    base64_image_str = request.data.get('image')

    base64_image = base64_image_str

    decoded_image_data = base64.b64decode(base64_image)

    image = Image.open(BytesIO(decoded_image_data))

    media_root = MEDIA_ROOT

    image_filename = 'your_file.jpg'
    print("Image is received")
    image_path = os.path.join(media_root, image_filename)

    image.save(image_path)

    text = "ijeqhd 3qhodjhqw  johdqw j"

    user_data = []
    user_data.append({
        'text': text
    })

    return Response(user_data)


@api_view(['POST'])
def text(request):
    biology_paragraph = request.data.get('text')

    themes = [
        'Cell Biology',
        'Genetics',
        'Ecology',
        'Human Physiology',
        'Evolution',
        'Plant Biology',
        'Human Health and Disease',
        'Enzymes',
        'Reproduction',
        'Biotechnology'
    ]


    def classify_mistake(paragraph):
        input_text = 'Here are 10 biology themes:'.join(themes) + '\n Your task is to read paragraph below ' \
                                                                  'and write the name of theme from previous themes, which is recommended to revise' + paragraph

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=input_text,
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        predicted_theme = response.choices[0].text.strip()


        input_text1 = 'Here are 10 biology themes:'.join(themes) + '\n Your task is to read paragraph below ' \
                                                              'and write where exactly i have mistakes and give recommendations' + paragraph
        # Use OpenAI API to generate the classification
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=input_text1,
            max_tokens=600,
            n=1,
            stop=None,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the predicted theme
        rec = response.choices[0].text.strip()


        questions = 'What are the differences between prokaryotic and eukaryotic cells? Provide examples of each. Describe the structure and function of the cell membrane." "Explain the process of cell division in eukaryotic cells.""Discuss the role of endoplasmic reticulum in protein synthesis." "How does the Golgi apparatus contribute to the packaging and transport of cellular products?" "What is the difference between genotype and phenotype? Provide examples." "Explain the inheritance pattern of sex-linked traits." "Discuss the concept of codominance and provide an example." "Describe the process of DNA replication and its significance in heredity." "How does crossing over contribute to genetic variation during meiosis?""'

    
        # Concatenate the themes and paragraph
        input_text = 'Here are 10 biology themes:'.join(themes) + '\n Your task is to read paragraph below ' \
                                                                'find my mistakes and weak sides. And create 10 questions like' + questions + paragraph


        # Use OpenAI API to generate the classification
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=input_text,
            max_tokens=600,
            n=1,
            stop=None,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the predicted theme
        generatedquestions = response.choices[0].text.strip()

        return [predicted_theme, rec, generatedquestions]


    biology_paragraph = "Cell Biology, Genetics, Ecology, Human Physiology, Evolution, Plant Biology, Human Health and Disease, Enzymes, Reproduction, and Biotechnology are all fascinating themes in the field of biology. Cell Biology explores the structure and function of cells, which are the fundamental units of life. Genetics delves into the study of heredity and the role of genes in determining traits. Ecology examines the interactions between organisms and their environment. Human Physiology focuses on the functioning of the human body's various systems. Evolution explains the process of species change over time through natural selection. Plant Biology investigates the life processes and adaptations of plants. Human Health and Disease explores the factors that influence well-being and the development of illnesses. Enzymes are crucial biological catalysts that facilitate chemical reactions in living organisms. Reproduction is the process by which living organisms produce offspring. Finally, Biotechnology involves the use of biological systems and organisms to develop useful products and technologies."
    mistake_theme = (classify_mistake(biology_paragraph))

    filtered_questions = Questions.objects.filter(theme=mistake_theme[0])

    question_list = [
        {'theme': question.theme, 'question': question.question}
        for question in filtered_questions
    ]


    response_data = []
    response_data.append({
        'rec': mistake_theme[1],
        'sui': mistake_theme[2],
        'questions': question_list
    })


    return Response(response_data)


