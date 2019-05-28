variable "project" {
  default = "Usecase"
}

variable "environment" {
  default = "EnvUsecase"
}

variable "name" {
  default = "My terraform cluster with python"
}

variable "vpc_id" {
  default = "vpc-603ab518"
}

variable "release_label" {
  default = "emr-5.23.0"
}

variable "applications" {
  default = ["Spark","JupyterHub","Hadoop","Hive","Hue","Pig","Zeppelin"]
  type    = "list"
}

variable "subnet_id" {
  default = "subnet-14169f5f"
}

variable "instance_groups" {
  default = [
    {
      name           = "MasterInstanceGroup"
      instance_role  = "MASTER"
      instance_type  = "m4.large"
      instance_count = 1
    },
    {
      name           = "CoreInstanceGroup"
      instance_role  = "CORE"
      instance_type  = "m4.large"
      instance_count = "2"
    },
  ]

  type = "list"
}

variable "bootstrap_name" {
  default = "pandas"
}

variable "bootstrap_uri" {
  default = "s3://seedingflow-usecase/install_my_librairies.sh"
}

variable "bootstrap_args" {
  default = []
  type    = "list"
}

variable "log_uri" {
  default = "s3://seedingflow-usecase/"
}

variable "python_path" {
  default = "s3://seedingflow-usecase/getClustersSpark.py"
}

variable "python_args" {
  default = ["s3://seedingflow-usecase/cases.json","s3://seedingflow-usecase/outputT.json"]
  type    = "list"
}