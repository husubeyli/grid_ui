from django.apps import AppConfig
from django.apps import AppConfig
import subprocess
import os


GITHUB_REPO = 'https://github.com/elgun87/googleTest.git'
# MAVEN_PROJECT_PATH = '/tmp/adidas_with_cucumber'
MAVEN_PROJECT_PATH = '/Users/husubayli/Desktop/Documents/test_folders/googleTest'


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Projeyi server başlatıldığında klonla/güncelle
        if not os.path.exists(MAVEN_PROJECT_PATH):
            clone_command = ['git', 'clone', GITHUB_REPO, MAVEN_PROJECT_PATH]
        else:
            clone_command = ['git', '-C', MAVEN_PROJECT_PATH, 'pull']

        try:
            subprocess.run(clone_command, check=True,
                           capture_output=True, text=True)
            print("GitHub projesi başarıyla klonlandı/güncellendi.")
        except subprocess.CalledProcessError as e:
            print("GitHub klonlama/güncelleme hatası:", e.stderr)
