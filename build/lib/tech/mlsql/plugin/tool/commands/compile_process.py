import re
import os
import glob
import jinja2
import shutil


class BaseSpark(object):
    def pom_convert(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(self.current_path, '.repo')))
        template_name = "pom.template.xml"
        template = env.get_template(template_name)
        pom_xml = template.render(spark_binary_version=self.spark_binary_version,
                                  spark_version=self.spark_version,
                                  scala_version=self.scala_version,
                                  scala_binary_version=self.scala_binary_version,
                                  arrow_version=self.arrow_version
                                  )
        with open("pom.xml", "w") as f:
            f.writelines(pom_xml)

    def source_convert(self):
        parent_path = os.path.join(os.getcwd(), ".repo", self.name, "source")
        target_path = os.path.join(os.getcwd(), "src", "main", "java")
        files = glob.glob(os.path.join(parent_path, "**", "*.scala"), recursive=True)
        for file in files:
            print(f"copy {file} to {file.replace(parent_path, target_path)}")
            shutil.copyfile(file, file.replace(parent_path, target_path))


class Spark311(BaseSpark):
    def __init__(self, current_path=os.getcwd()):
        self.spark_binary_version = "3.0"
        self.spark_version = "3.1.1"
        self.scala_version = "2.12.10"
        self.scala_binary_version = "2.12"
        self.arrow_version = "2.0.0"
        self.name = "311"
        self.current_path = current_path


class Spark243(BaseSpark):
    def __init__(self, current_path=os.getcwd()):
        self.spark_binary_version = "2.4"
        self.spark_version = "2.4.3"
        self.scala_version = "2.11.12"
        self.scala_binary_version = "2.11"
        self.arrow_version = "0.10.0"
        self.name = "243"
        self.current_path = current_path


class Utils(object):
    @staticmethod
    def cleantag(raw: str) -> str:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw)
        return cleantext
