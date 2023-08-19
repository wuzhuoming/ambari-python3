"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management.libraries.script import Script
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.security_commons import build_expectations, \
  cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
  FILE_TYPE_XML
from scripts.hdfs_nfsgateway import nfsgateway
from scripts.hdfs import hdfs
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions.stack_features import check_stack_feature


class NFSGateway(Script):
  def install(self, env):
    from scripts import params

    env.set_params(params)

    self.install_packages(env)

  def pre_upgrade_restart(self, env, upgrade_type=None):
    from scripts import params
    env.set_params(params)

    if params.stack_version_formatted and check_stack_feature(StackFeature.NFS, params.stack_version_formatted):
      stack_select.select_packages(params.version)

  def start(self, env, upgrade_type=None):
    from scripts import params
    env.set_params(params)

    self.configure(env)
    nfsgateway(action="start")

  def stop(self, env, upgrade_type=None):
    from scripts import params
    env.set_params(params)

    nfsgateway(action="stop")

  def configure(self, env):
    from scripts import params

    env.set_params(params)
    hdfs()
    nfsgateway(action="configure")

  def status(self, env):
    from scripts import status_params

    env.set_params(status_params)

    check_process_status(status_params.nfsgateway_pid_file)
      
  def get_log_folder(self):
    from scripts import params
    return params.hdfs_log_dir
  
  def get_user(self):
    from scripts import params
    return params.hdfs_user

  def get_pid_files(self):
    from scripts import status_params
    return [status_params.nfsgateway_pid_file]

if __name__ == "__main__":
  NFSGateway().execute()
