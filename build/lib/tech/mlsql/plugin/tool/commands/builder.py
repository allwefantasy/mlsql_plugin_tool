import pathlib

from tech.mlsql.plugin.tool.shellutils import run_cmd


class PluginBuilder(object):
    def __init__(self,
                 mvn: str,
                 module_name: str
                 ):
        self.mvn = mvn
        self.module_name = module_name

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
            ab_file_path = "{}/{}/target/{}".format(full_path, self.module_name,
                                                    "{}_{}-{}.jar".format(jar_name, scala_version,
                                                                          version))
            jarPaths.append(ab_file_path)

        print("====Build success!=====")
        i = 0
        for jarPath in jarPaths:
            print(" File location {}：\n {}".format(i, jarPath))
            i += 1
