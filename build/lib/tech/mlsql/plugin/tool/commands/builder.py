import os
import pathlib
import shutil

import jinja2

from tech.mlsql.plugin.tool.commands.compile_process import Spark311, Spark243
from tech.mlsql.plugin.tool.shellutils import run_cmd


class PluginBuilder(object):
    def __init__(self,
                 mvn: str,
                 module_name: str,
                 spark: str
                 ):
        self.mvn = mvn
        self.module_name = module_name
        # spark311 / spark243
        self.spark = spark

    def plugin_desc_convert(self, current_path: str):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(current_path, '.repo')))
        template_name = "plugin.template.desc"
        template = env.get_template(template_name)
        plugin_desc = template.render(spark_binary_version=self.spark_binary_version,
                                      spark_version=self.spark_version,
                                      scala_version=self.scala_version,
                                      scala_binary_version=self.scala_binary_version
                                      )
        with open("plugin.desc", "w") as f:
            f.writelines(plugin_desc)

    def convert(self):
        for root, dirs, files in os.walk(os.getcwd()):
            self._convert(root)
            for module in dirs:
                module_path = os.path.join(root, module)
                self._convert(module_path)
                self.plugin_desc_convert(module_path)

    def _convert(self, current_path: str):
        if not os.path.exists(os.path.join(current_path, ".repo")):
            return
        if self.spark == "spark311":
            builder = Spark311()
        elif self.spark == "spark243":
            builder = Spark243()
        else:
            raise Exception(f"spark {self.spark} is not support ")
        builder.pom_convert()
        builder.source_convert()

    def build(self):
        group = []
        with open("./{}/desc.plugin".format(self.module_name), "r") as f:
            config = {}
            for line in f.readlines():
                if line and line.strip():
                    clean_line = line.strip()
                    if clean_line == "__SPLITTER__":
                        group.append(config)
                        config = {}
                    else:
                        (k, v) = clean_line.split("=", 1)
                        config[k] = v
            group.append(config)
        jarPaths = []
        for config in group:
            plugin_name = config.get("moduleName") or self.module_name
            version = config["version"]
            scala_version = config["scala_version"]
            spark_version = "spark_version" in config and config["spark_version"]

            if not self.mvn:
                self.mvn = "mvn"

            spark_params = []
            if spark_version:
                spark_params = ["-Pspark-{}".format(spark_version)]
            command = [self.mvn, "-DskipTests", "clean",
                       "package", "-Pshade", ] + spark_params + ["-Pscala-{}".format(scala_version)] + ["-pl",
                                                                                                        self.module_name]
            run_cmd(command)
            jar_name = self.module_name
            if spark_version:
                jar_name = self.module_name + "-" + spark_version
            full_path = pathlib.Path().absolute()
            jar_final_name = "{}_{}-{}.jar".format(jar_name, scala_version, version)
            ab_file_path = os.path.join(full_path, self.module_name, "target",
                                        jar_final_name)
            build_path = os.path.join(full_path, self.module_name, "build")
            target_file = os.path.join(build_path, jar_final_name)
            if not os.path.exists(build_path):
                os.mkdir(build_path)
                shutil.copyfile(ab_file_path, target_file)
            jarPaths.append(target_file)

        print("====Build success!=====")
        i = 0
        for jarPath in jarPaths:
            print(" File location {}：\n {}".format(i, jarPath))
            i += 1
