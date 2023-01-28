# my_own_collection
# Домашнее задание к занятию "6.Создание собственных модулей"

## Подготовка к выполнению
1. Создайте пустой публичных репозиторий в любом своём проекте: `my_own_collection`
2. Скачайте репозиторий ansible: `git clone https://github.com/ansible/ansible.git` по любому удобному вам пути
3. Зайдите в директорию ansible: `cd ansible`
4. Создайте виртуальное окружение: `python3 -m venv venv`
5. Активируйте виртуальное окружение: `. venv/bin/activate`. Дальнейшие действия производятся только в виртуальном окружении
6. Установите зависимости `pip install -r requirements.txt`
7. Запустить настройку окружения `. hacking/env-setup`
8. Если все шаги прошли успешно - выйти из виртуального окружения `deactivate`
9. Ваше окружение настроено, для того чтобы запустить его, нужно находиться в директории `ansible` и выполнить конструкцию `. venv/bin/activate && . hacking/env-setup`

## Основная часть

Наша цель - написать собственный module, который мы можем использовать в своей role, через playbook. Всё это должно быть собрано в виде collection и отправлено в наш репозиторий.

1. В виртуальном окружении создать новый `my_own_module.py` файл
2. Наполнить его содержимым:
```python
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```
Или возьмите данное наполнение из [статьи](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#creating-a-module).

3. Заполните файл в соответствии с требованиями ansible так, чтобы он выполнял основную задачу: module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.
4. Проверьте module на исполняемость локально.
5. Напишите single task playbook и используйте module в нём.
6. Проверьте через playbook на идемпотентность.
7. Выйдите из виртуального окружения.
8. Инициализируйте новую collection: `ansible-galaxy collection init my_own_namespace.yandex_cloud_elk`
9. В данную collection перенесите свой module в соответствующую директорию.
10. Single task playbook преобразуйте в single task role и перенесите в collection. У role должны быть default всех параметров module
11. Создайте playbook для использования этой role.
12. Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег `1.0.0` на этот коммит.
13. Создайте .tar.gz этой collection: `ansible-galaxy collection build` в корневой директории collection.
14. Создайте ещё одну директорию любого наименования, перенесите туда single task playbook и архив c collection.
15. Установите collection из локального архива: `ansible-galaxy collection install <archivename>.tar.gz`
16. Запустите playbook, убедитесь, что он работает.
17. В ответ необходимо прислать ссылку на репозиторий с collection

## Необязательная часть

1. Реализуйте свой собственный модуль для создания хостов в Yandex Cloud.
2. Модуль может (и должен) иметь зависимость от `yc`, основной функционал: создание ВМ с нужным сайзингом на основе нужной ОС. Дополнительные модули по созданию кластеров Clickhouse, MySQL и прочего реализовывать не надо, достаточно простейшего создания ВМ.
3. Модуль может формировать динамическое inventory, но данная часть не является обязательной, достаточно, чтобы он делал хосты с указанной спецификацией в YAML.
4. Протестируйте модуль на идемпотентность, исполнимость. При успехе - добавьте данный модуль в свою коллекцию.
5. Измените playbook так, чтобы он умел создавать инфраструктуру под inventory, а после устанавливал весь ваш стек Observability на нужные хосты и настраивал его.
6. В итоге, ваша коллекция обязательно должна содержать: clickhouse-role(если есть своя), lighthouse-role, vector-role, два модуля: my_own_module и модуль управления Yandex Cloud хостами и playbook, который демонстрирует создание Observability стека.

---
## Ответ 

Коллекция выложена в текущий репозиторий (my_own_collection)[https://github.com/VovetZ/my_own_collection]

Далее описание выполненных действий

- Подготовка 

```bash
root@vkvm:/home/vk# mkdir tmp_ansible
root@vkvm:/home/vk# cd tmp_ansible/
root@vkvm:/home/vk/tmp_ansible# git clone https://github.com/ansible/ansible.git
Cloning into 'ansible'...
remote: Enumerating objects: 589343, done.
remote: Counting objects: 100% (259/259), done.
remote: Compressing objects: 100% (207/207), done.
remote: Total 589343 (delta 104), reused 138 (delta 36), pack-reused 589084
Receiving objects: 100% (589343/589343), 225.53 MiB | 9.78 MiB/s, done.
Resolving deltas: 100% (392676/392676), done.
root@vkvm:/home/vk/tmp_ansible# cd ansible/
root@vkvm:/home/vk/tmp_ansible/ansible# python3 -m venv venv
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.10-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: ['/home/vk/tmp_ansible/ansible/venv/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']

root@vkvm:/home/vk/tmp_ansible/ansible# apt install python3.10-venv
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  python3-pip-whl python3-setuptools-whl
The following NEW packages will be installed:
  python3-pip-whl python3-setuptools-whl python3.10-venv
0 upgraded, 3 newly installed, 0 to remove and 36 not upgraded.
Need to get 2 473 kB of archives.
After this operation, 2 882 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
..........................................
Setting up python3-setuptools-whl (59.6.0-1.2) ...
Setting up python3-pip-whl (22.0.2+dfsg-1) ...
Setting up python3.10-venv (3.10.6-1~22.04.2) ...
root@vkvm:/home/vk/tmp_ansible/ansible# python3 -m venv venv
root@vkvm:/home/vk/tmp_ansible/ansible# . venv/bin/activate
(venv) root@vkvm:/home/vk/tmp_ansible/ansible# pip install -r requirements.txt 
Ignoring importlib_resources: markers 'python_version < "3.10"' don't match your environment
...................................
Installing collected packages: resolvelib, PyYAML, pycparser, packaging, MarkupSafe, jinja2, cffi, cryptography
Successfully installed MarkupSafe-2.1.1 PyYAML-6.0 cffi-1.15.1 cryptography-39.0.0 jinja2-3.1.2 packaging-23.0 pycparser-2.21 resolvelib-0.9.0
(venv) root@vkvm:/home/vk/tmp_ansible/ansible# . hacking/env-setup
running egg_info
........................................
Setting up Ansible to run out of checkout...

PATH=/home/vk/tmp_ansible/ansible/bin:/home/vk/tmp_ansible/ansible/venv/bin:/root/yandex-cloud/bin:/root/yandex-cloud/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
PYTHONPATH=/home/vk/tmp_ansible/ansible/test/lib:/home/vk/tmp_ansible/ansible/lib
MANPATH=/home/vk/tmp_ansible/ansible/docs/man:/usr/local/man:/usr/local/share/man:/usr/share/man

Remember, you may wish to specify your host file with -i

Done!
```

- В виртуальном окружении создадим новый `my_own_module.py` файл
    ```bash
    vim lib/ansible/modules/my_own_module.py
    ```
- Подготовим load.json, который будем передавать модулю
    ```json
   {
    "ANSIBLE_MODULE_ARGS": {
        "path": "vk_test_file.txt",
        "content": "Everything is OK!!!!!!"
        }
   }
    ```
- Проверим модуль локально 
    ```bash
   (venv) root@vkvm:/home/vk/tmp_ansible/ansible# python3 -m ansible.modules.my_own_module load.json

{"changed": true, "message": "File vk_test_file.txt created/overwrited with new content", "invocation": {"module_args": {"path": "vk_test_file.txt", "content": "Everything is OK!!!!!!"}}}

   ```
- Файл создался
```bash
  (venv) root@vkvm:/home/vk/tmp_ansible/ansible# cat vk_test_file.txt 
        Everything is OK!!!!!!!
```
- Создадим playbook `test_playbook.yml`

```yaml
---
- name: Import my_own_module 
  hosts: localhost
  tasks:
  - name: Run my_own_module
    my_own_module:
      path: './vk_playbook_test_file.txt'
      content: "Playbook test content. OK!"
```

- Проиграем playbook и проверим результат 
```bash
(venv) root@vkvm:/home/vk/tmp_ansible/ansible# ansible-playbook --connection=local --inventory localhost test_playbook.yml 
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.
[WARNING]: Unable to parse /home/vk/tmp_ansible/ansible/localhost as an inventory source
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does
not match 'all'

PLAY [Import my_own_module] ***********************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [localhost]

TASK [Run my_own_module] **************************************************************************************
ok: [localhost]

PLAY RECAP ****************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
(venv) root@vkvm:/home/vk/tmp_ansible/ansible# cat vk_playbook_test_file.txt 
Playbook test content. OK!
```

- Выход из venv
```
    deactivate
```
- Инициализация новой коллекции
```bash
root@vkvm:/home/vk/tmp_ansible/ansible# cd ..
root@vkvm:/home/vk/tmp_ansible# ansible-galaxy collection init my_own_namespace.vk_collection
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if
you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing
source of code and can become unstable at any point.
- Collection my_own_namespace.vk_collection was created successfully
```

- Скопируем в коллекцию созданный модуль

```bash
    root@vkvm:/home/vk/tmp_ansible# mkdir -p my_own_namespace/vk_collection/plugins/modules
    root@vkvm:/home/vk/tmp_ansible# cp ansible/lib/ansible/modules/my_own_module.py my_own_namespace/vk_collection/plugins/modules/
```

- Создадим роль 

```bash
    root@vkvm:/home/vk/tmp_ansible# cd my_own_namespace/vk_collection/roles/
root@vkvm:/home/vk/tmp_ansible/my_own_namespace/vk_collection/roles# ansible-galaxy role init my_own_role
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if
you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing
source of code and can become unstable at any point.
- Role my_own_role was created successfully
```
- Меняем файл переменных по умолчанию в файле `defaults/main.yml`

```yml
    ---
    # defaults file for my_own_role
    path: './vk_test_role_file.txt'
    content: "test content for own role test"
```
-  Меняем задачи в файле `tasks/main.yml`

```yml
    ---
    # tasks file for my_own_role
    - name: Create file
      my_own_module:
        path: "{{ path }}"
        content: "{{ content }}"
```

- Создадим плейбук `my_own_playbook.yml` для проигрывания роли 

```yml
    ---
    - name: Import my_own_role
      hosts: localhost
      roles:
        - role: my_own_role
```

- Проверим модуль в коллекции

```bash
root@vkvm:/home/vk/tmp_ansible/my_own_namespace/vk_collection# ANSIBLE_LIBRARY=./plugins/modules
root@vkvm:/home/vk/tmp_ansible/my_own_namespace/vk_collection/roles# ansible -m my_own_module -a 'path=./collection_test_file.txt content="My collection test content!!!"' localhost
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.
localhost | CHANGED => {
    "changed": true,
    "message": "File ./collection_test_file.txt created/overwrited with new content"
}
```

- Проиграем playbook

```bash
root@vkvm:/home/vk/tmp_ansible/my_own_namespace/vk_collection# ansible-playbook --connection=local --inventory localhost my_own_playbook.yml
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.
[WARNING]: Unable to parse /home/vk/tmp_ansible/my_own_namespace/vk_collection/localhost as an inventory
source
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does
not match 'all'

PLAY [Import my_own_role] *************************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [localhost]

TASK [my_own_role : Create file] ******************************************************************************
ok: [localhost]

PLAY RECAP ****************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

- Создадим архив коллекции
```bash
rroot@vkvm:/home/vk/tmp_ansible/my_own_namespace/vk_collection# ansible-galaxy collection build --force
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.
Created collection for my_own_namespace.vk_collection at /home/vk/tmp_ansible/my_own_namespace/vk_collection/my_own_namespace-vk_collection-1.0.0.tar.gz
```
- Установим коллекцию из архива  в новую директорию для тестирования

```bash
root@vkvm:/home/vk/tmp_ansible# mkdir collection_test_2
root@vkvm:/home/vk/tmp_ansible# cd collection_test_2
root@vkvm:/home/vk/tmp_ansible/collection_test_2# cp ../my_own_namespace/vk_collection/my_own_namespace-vk_collection-1.0.0.tar.gz .
root@vkvm:/home/vk/tmp_ansible/collection_test_2# ansible-galaxy collection install my_own_namespace-vk_collection-1.0.0.tar.gz 
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.
Starting galaxy collection install process
Nothing to do. All requested collections are already installed. If you want to reinstall them, consider using `--force`.
root@vkvm:/home/vk/tmp_ansible/collection_test_2# ansible-galaxy collection install my_own_namespace-vk_collection-1.0.0.tar.gz --force
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'my_own_namespace.vk_collection:1.0.0' to '/root/.ansible/collections/ansible_collections/my_own_namespace/vk_collection'
my_own_namespace.vk_collection:1.0.0 was installed successfully
root@vkvm:/home/vk/tmp_ansible/collection_test_2# cd ~/.ansible/collections/ansible_collections/my_own_namespace/vk_collection
root@vkvm:~/.ansible/collections/ansible_collections/my_own_namespace/vk_collection# 
```
- Проиграем playbook из коллекции, проверим что нужный файл появился

```bash
root@vkvm:~/.ansible/collections/ansible_collections/my_own_namespace/vk_collection# ansible-playbook --connection=local --inventory localhost, my_own_playbook.yml
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you
are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source
of code and can become unstable at any point.

PLAY [Import my_own_role] *************************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [localhost]

TASK [my_own_namespace.vk_collection.my_own_role : Create file] ***********************************************
ok: [localhost]

PLAY RECAP ****************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@vkvm:~/.ansible/collections/ansible_collections/my_own_namespace/vk_collection# cat collection_test_file.txt 
My collection test content!!!
```
