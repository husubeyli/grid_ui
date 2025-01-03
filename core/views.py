from django.shortcuts import render
import subprocess
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import TestCase
import os
# MAVEN_PROJECT_PATH = '/path/to/maven/project'  # Maven projenizin yolu

GITHUB_REPO = 'https://github.com/elgun87/googleTest.git'
# MAVEN_PROJECT_PATH = '/tmp/adidas_with_cucumber'
MAVEN_PROJECT_PATH = '/Users/husubayli/Desktop/Documents/test_folders/googleTest'




@csrf_exempt
@api_view(['POST'])
def trigger_test(request):
    test_id = request.data.get('test_id')

    try:
        test_case = TestCase.objects.get(id=test_id)
    except TestCase.DoesNotExist:
        return Response({"error": "Test Vakası Bulunamadı"}, status=404)

    # Selenium Grid URL'si
    grid_url = settings.SELENIUM_GRID_URL

    # Maven komutunu çalıştır
    # command = [
    #     'mvn',
    #     'clean',
    #     'compile',
    #     'test',
    #     '-Dselenium.grid.url=' + grid_url,
    #     f'-Dtest={test_case.name}',
    #     '-Dtest=GoogleTest'
    #     # '-Dsurefire.suiteXmlFiles=src/test/resources/testng.xml'

    # ]
    command = [
        'mvn',
        'clean',
        'test',
        '-Dselenium.grid.url=' + grid_url,
        '-Dsurefire.suiteXmlFiles=src/test/resources/testng.xml'
        # f'-Dtest={test_case.name}',
        # '-Dtest=GoogleTest'  # Test sınıfını doğrudan çalıştır
    ]

    print("Maven komutu:", command)
    try:
        result = subprocess.run(
            command,
            cwd=MAVEN_PROJECT_PATH,  # Maven komuxtunu projenin içinde çalıştır
            capture_output=True,
            text=True,
            timeout=120  # 2 dakika sınır
        )
        print(100*'#')
        print("STDOUT:", result.stdout)
        print(100*'*')
        print("STDERR:", result.stderr)
        print(os.path.exists(MAVEN_PROJECT_PATH)) 
        
        # Maven çıktısını veritabanına kaydet
        test_case.execution_result = result.stdout
        test_case.status = 'Başarılı' if result.returncode == 0 else 'Başarısız'
        test_case.save()

        return Response({
            "message": "Test başarıyla çalıştırıldı",
            "output": result.stdout
        })

    except subprocess.CalledProcessError as e:
        print(e, 'error_var')
        return Response({
            "error": "Maven testi başlatılamadı",
            "details": e.stderr
        }, status=500)



class HomePageView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Veritabanından tüm test vakalarını çekiyoruz
        context['test_cases'] = TestCase.objects.all()
        return context
