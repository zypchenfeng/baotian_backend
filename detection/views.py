from .serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os
# Create your views here.
from .detection_model import detection_main
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import json
from .output_json import to_txt_files 


server_url = "http://jyzn.nat300.top/"
annotation_path = './media/annotations/'

@csrf_exempt
def test(request):
    if request.method=="POST":
        res = request.FILES['file']
        res = json.load(res)
        to_txt_files(res,annotation_path)
    return HttpResponse("succeed")

class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            #保存到数据库
            posts_serializer.save()
            
            #获得本地图片地址
            image = posts_serializer.data["image"][1:]
            
            #获得图片名称
            dir_path,full_file_name = os.path.split(image)
            file_name, extension = os.path.splitext(full_file_name)


            
            #调用培训好的算法
            detection_result, output_image = detection_main(image,"media/output_images/"+file_name)
            
            #with open(output_image, 'rb') as f:
            #    image_data = f.read()
            response_url = os.path.join(server_url,output_image)
            
            return HttpResponse(response_url)
            # return HttpResponse(image_data, content_type="image/jpeg")
            # return Response(posts_serializer.data)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)











