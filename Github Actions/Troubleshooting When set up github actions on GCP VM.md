```shell
[dev@services-server backend-docker]$ pwd
/srv/devs/backend-docker
[dev@services-server backend-docker]$ cd ../.
[dev@services-server ~]$ ll\
> ^C
[dev@services-server ~]$ mkdir actions-runner && cd actions-runner
[dev@services-server actions-runner]$ curl -o actions-runner-linux-x64-2.330.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.330.0/actions-runner-linux-x64-2.330.0.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  211M  100  211M    0     0   193M      0  0:00:01  0:00:01 --:--:--  231M
[dev@services-server actions-runner]$ echo "af5c33fa94f3cc33b8e97937939136a6b04197e6dadfcfb3b6e33ae1bf41e79a  actions-runner-linux-x64-2.330.0.tar.gz" | shasum -a 256 -c
-bash: shasum: command not found
[dev@services-server actions-runner]$ tar xzf ./actions-runner-linux-x64-2.330.0.tar.gz
[dev@services-server actions-runner]$ ./config.sh --url https://github.com/ThatboxAI/backend-docker --token AE35NMBCE74U4JG7TIZZ7ILJMTZT4

--------------------------------------------------------------------------------
|        ____ _ _   _   _       _          _        _   _                      |
|       / ___(_) |_| | | |_   _| |__      / \   ___| |_(_) ___  _ __  ___      |
|      | |  _| | __| |_| | | | | '_ \    / _ \ / __| __| |/ _ \| '_ \/ __|     |
|      | |_| | | |_|  _  | |_| | |_) |  / ___ \ (__| |_| | (_) | | | \__ \     |
|       \____|_|\__|_| |_|\__,_|_.__/  /_/   \_\___|\__|_|\___/|_| |_|___/     |
|                                                                              |
|                       Self-hosted runner registration                        |
|                                                                              |
--------------------------------------------------------------------------------

# Authentication


√ Connected to GitHub

# Runner Registration

Enter the name of the runner group to add this runner to: [press Enter for Default] thinkbox_self_hosted_runner

Could not find any self-hosted runner group named "thinkbox_self_hosted_runner".
[dev@services-server actions-runner]$ ./config.sh --url https://github.com/ThatboxAI/backend-docker --token AE35NMBCE74U4JG7TIZZ7ILJMTZT4

--------------------------------------------------------------------------------
|        ____ _ _   _   _       _          _        _   _                      |
|       / ___(_) |_| | | |_   _| |__      / \   ___| |_(_) ___  _ __  ___      |
|      | |  _| | __| |_| | | | | '_ \    / _ \ / __| __| |/ _ \| '_ \/ __|     |
|      | |_| | | |_|  _  | |_| | |_) |  / ___ \ (__| |_| | (_) | | | \__ \     |
|       \____|_|\__|_| |_|\__,_|_.__/  /_/   \_\___|\__|_|\___/|_| |_|___/     |
|                                                                              |
|                       Self-hosted runner registration                        |
|                                                                              |
--------------------------------------------------------------------------------

# Authentication


√ Connected to GitHub

# Runner Registration

Enter the name of the runner group to add this runner to: [press Enter for Default]

Enter the name of runner: [press Enter for services-server] thinkbox_self_hosted_runner

This runner will have the following labels: 'self-hosted', 'Linux', 'X64'
Enter any additional labels (ex. label-1,label-2): [press Enter to skip] thinkbox_self_hosted_runner

√ Runner successfully added

# Runner settings

Enter name of work folder: [press Enter for _work]

√ Settings Saved.

[dev@services-server actions-runner]$ ./run.sh

√ Connected to GitHub

Current runner version: '2.330.0'
2026-01-12 12:30:21Z: Listening for Jobs
^CExiting...
Runner listener exit with 0 return code, stop the service, no retry needed.
Exiting runner...
[dev@services-server actions-runner]$ pwd
/srv/devs/actions-runner
[dev@services-server actions-runner]$ pll
-bash: pll: command not found
[dev@services-server actions-runner]$ ll
total 216840
-rw-r--r--. 1 dev devs 221990519 Jan 12 12:28 actions-runner-linux-x64-2.330.0.tar.gz
drwxr-sr-x. 4 dev devs     12288 Nov 19 14:35 bin
-rwxr-xr-x. 1 dev devs      2458 Nov 19 14:34 config.sh
drwxr-sr-x. 2 dev devs       120 Jan 12 12:30 _diag
-rwxr-xr-x. 1 dev devs       646 Nov 19 14:34 env.sh
drwxr-sr-x. 6 dev devs        76 Nov 19 14:35 externals
-rw-r--r--. 1 dev devs      1619 Nov 19 14:34 run-helper.cmd.template
-rwxr-xr-x. 1 dev devs      2663 Jan 12 12:30 run-helper.sh
-rwxr-xr-x. 1 dev devs      2663 Nov 19 14:34 run-helper.sh.template
-rwxr-xr-x. 1 dev devs      2535 Nov 19 14:34 run.sh
-rwxr-xr-x. 1 dev devs        66 Nov 19 14:34 safe_sleep.sh
-rwxr-xr-x. 1 dev devs      5270 Jan 12 12:30 svc.sh
[dev@services-server actions-runner]$ ./svc.sh install  dev
Must run as sudo
[dev@services-server actions-runner]$ sudo ./svc.sh install  dev
Creating launch runner in /etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
Run as user: dev
Run as uid: 1002
gid: 1003
Relabeled /etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service from unconfined_u:object_r:var_t:s0 to unconfined_u:object_r:systemd_unit_file_t:s0
Created symlink /etc/systemd/system/multi-user.target.wants/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service → /etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service.
[dev@services-server actions-runner]$ sudo ./svc.sh start

/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
× actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service - GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner)
     Loaded: loaded (/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service; enabled; preset: disabled)
     Active: failed (Result: exit-code) since Mon 2026-01-12 12:32:45 UTC; 329ms ago
   Duration: 10ms
    Process: 1221703 ExecStart=/srv/devs/actions-runner/runsvc.sh (code=exited, status=203/EXEC)
   Main PID: 1221703 (code=exited, status=203/EXEC)
        CPU: 3ms

Jan 12 12:32:45 services-server systemd[1]: Started GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner).
Jan 12 12:32:45 services-server systemd[1221703]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed to locate executable /srv/dev…ssion denied
Jan 12 12:32:45 services-server systemd[1221703]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed at step EXEC spawning /srv/de…ssion denied
Jan 12 12:32:45 services-server systemd[1]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Main process exited, code=exited, status=203/EXEC
Jan 12 12:32:45 services-server systemd[1]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed with result 'exit-code'.
Hint: Some lines were ellipsized, use -l to show in full.
[dev@services-server actions-runner]$ sudo ./svc.sh status

/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
× actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service - GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner)
     Loaded: loaded (/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service; enabled; preset: disabled)
     Active: failed (Result: exit-code) since Mon 2026-01-12 12:32:45 UTC; 46s ago
   Duration: 10ms
    Process: 1221703 ExecStart=/srv/devs/actions-runner/runsvc.sh (code=exited, status=203/EXEC)
   Main PID: 1221703 (code=exited, status=203/EXEC)
        CPU: 3ms

Jan 12 12:32:45 services-server systemd[1]: Started GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner).
Jan 12 12:32:45 services-server systemd[1221703]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed to locate executable /srv/dev…ssion denied
Jan 12 12:32:45 services-server systemd[1221703]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed at step EXEC spawning /srv/de…ssion denied
Jan 12 12:32:45 services-server systemd[1]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Main process exited, code=exited, status=203/EXEC
Jan 12 12:32:45 services-server systemd[1]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed with result 'exit-code'.
Hint: Some lines were ellipsized, use -l to show in full.
[dev@services-server actions-runner]$ sudo ./svc.sh status -l

/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
× actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service - GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner)
     Loaded: loaded (/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service; enabled; preset: disabled)
     Active: failed (Result: exit-code) since Mon 2026-01-12 12:32:45 UTC; 50s ago
   Duration: 10ms
    Process: 1221703 ExecStart=/srv/devs/actions-runner/runsvc.sh (code=exited, status=203/EXEC)
   Main PID: 1221703 (code=exited, status=203/EXEC)
        CPU: 3ms

Jan 12 12:32:45 services-server systemd[1]: Started GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner).
Jan 12 12:32:45 services-server systemd[1221703]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed to locate executable /srv/dev…ssion denied
Jan 12 12:32:45 services-server systemd[1221703]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed at step EXEC spawning /srv/de…ssion denied
Jan 12 12:32:45 services-server systemd[1]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Main process exited, code=exited, status=203/EXEC
Jan 12 12:32:45 services-server systemd[1]: actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service: Failed with result 'exit-code'.
Hint: Some lines were ellipsized, use -l to show in full.
[dev@services-server actions-runner]$ getenforce
Enforcing
[dev@services-server actions-runner]$ sudo setenforce 0
sudo ./svc.sh start

/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
● actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service - GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner)
     Loaded: loaded (/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service; enabled; preset: disabled)
     Active: active (running) since Mon 2026-01-12 12:39:19 UTC; 20ms ago
   Main PID: 1235491 ((unsvc.sh))
      Tasks: 1 (limit: 48872)
     Memory: 72.0K
        CPU: 1ms
     CGroup: /system.slice/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
             └─1235491 "(unsvc.sh)"

Jan 12 12:39:19 services-server systemd[1]: Started GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner).
[dev@services-server actions-runner]$ # 恢复/设置该目录的安全上下文
sudo chcon -R -t bin_t /srv/devs/actions-runner/
[dev@services-server actions-runner]$ sudo setenforce 1  # 记得把防火墙开回去
sudo ./svc.sh start
sudo ./svc.sh status

/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
● actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service - GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner)
     Loaded: loaded (/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service; enabled; preset: disabled)
     Active: active (running) since Mon 2026-01-12 12:39:19 UTC; 26s ago
   Main PID: 1235491 (runsvc.sh)
      Tasks: 20 (limit: 48872)
     Memory: 41.8M
        CPU: 1.780s
     CGroup: /system.slice/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
             ├─1235491 /bin/bash /srv/devs/actions-runner/runsvc.sh
             ├─1235494 ./externals/node20/bin/node ./bin/RunnerService.js
             └─1235501 /srv/devs/actions-runner/bin/Runner.Listener run --startuptype service

Jan 12 12:39:19 services-server systemd[1]: Started GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner).
Jan 12 12:39:19 services-server runsvc.sh[1235491]: .path=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
Jan 12 12:39:19 services-server runsvc.sh[1235494]: Starting Runner listener with startup type: service
Jan 12 12:39:19 services-server runsvc.sh[1235494]: Started listener process, pid: 1235501
Jan 12 12:39:19 services-server runsvc.sh[1235494]: Started running service
Jan 12 12:39:21 services-server runsvc.sh[1235494]: √ Connected to GitHub
Jan 12 12:39:22 services-server runsvc.sh[1235494]: Current runner version: '2.330.0'
Jan 12 12:39:22 services-server runsvc.sh[1235494]: 2026-01-12 12:39:22Z: Listening for Jobs

/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
● actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service - GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner)
     Loaded: loaded (/etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service; enabled; preset: disabled)
     Active: active (running) since Mon 2026-01-12 12:39:19 UTC; 26s ago
   Main PID: 1235491 (runsvc.sh)
      Tasks: 20 (limit: 48872)
     Memory: 41.8M
        CPU: 1.780s
     CGroup: /system.slice/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service
             ├─1235491 /bin/bash /srv/devs/actions-runner/runsvc.sh
             ├─1235494 ./externals/node20/bin/node ./bin/RunnerService.js
             └─1235501 /srv/devs/actions-runner/bin/Runner.Listener run --startuptype service

Jan 12 12:39:19 services-server systemd[1]: Started GitHub Actions Runner (ThatboxAI-backend-docker.thinkbox_self_hosted_runner).
Jan 12 12:39:19 services-server runsvc.sh[1235491]: .path=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
Jan 12 12:39:19 services-server runsvc.sh[1235494]: Starting Runner listener with startup type: service
Jan 12 12:39:19 services-server runsvc.sh[1235494]: Started listener process, pid: 1235501
Jan 12 12:39:19 services-server runsvc.sh[1235494]: Started running service
Jan 12 12:39:21 services-server runsvc.sh[1235494]: √ Connected to GitHub
Jan 12 12:39:22 services-server runsvc.sh[1235494]: Current runner version: '2.330.0'
Jan 12 12:39:22 services-server runsvc.sh[1235494]: 2026-01-12 12:39:22Z: Listening for Jobs
[dev@services-server actions-runner]$
```


这个报错 `status=203/EXEC` 配合 `Permission denied`，通常意味着 **Systemd 守护进程（root权限）在尝试执行启动脚本时被操作系统拦截了**。

既然你的路径在 `/srv/devs/...` 这种非标准系统目录下，**90% 的可能性是 SELinux 在捣乱**（如果你使用的是 CentOS/RHEL/Fedora/AlmaLinux 等系统）。

请按照以下步骤逐一排查解决：

### 第一步：检查并解决 SELinux 问题（最可能的原因）

Systemd 也就是系统的“管家”，它对安全非常敏感。如果 SELinux 处于开启状态（Enforcing），它会禁止 Systemd 去执行 `/srv` 目录下没有正确安全标签（Label）的脚本。

1. **检查 SELinux 状态**：
```bash
getenforce

```


* 如果输出 `Enforcing`，则几乎可以确定就是它的锅。
* 如果输出 `Disabled` 或 `Permissive`，请跳到第二步。


2. **临时验证**（如果上面是 Enforcing）：
你可以临时关闭 SELinux 看服务能否启动，以确认猜测：
```bash
sudo setenforce 0
sudo ./svc.sh start

```


如果这次成功启动了，说明确实是 SELinux 问题。记得之后要运行 `sudo ./svc.sh stop` 停止它，并继续下面的“永久修复”。
3. **永久修复（给文件贴上“可执行”的安全标签）**：
我们需要告诉 SELinux：“这个目录下的脚本是安全的二进制文件，允许运行”。
运行以下命令：
```bash
# 恢复/设置该目录的安全上下文
sudo chcon -R -t bin_t /srv/devs/actions-runner/

```


*解释：`bin_t` 是通用的可执行文件标签，告诉 SELinux 这里面是可以执行的程序。*
然后再次尝试启动服务：
```bash
sudo setenforce 1  # 记得把防火墙开回去
sudo ./svc.sh start
sudo ./svc.sh status

```



### 第二步：检查文件系统权限

如果不是 SELinux 的问题，可能是 Linux 的基本文件权限导致的。Systemd 虽然以 root 启动，但它会切换用户（通常切换回你安装 Runner 的用户 `dev`）。

1. **检查脚本是否有执行权限**：
确保 `runsvc.sh` 脚本本身是绿色的（可执行）：
```bash
sudo chmod +x /srv/devs/actions-runner/runsvc.sh

```


2. **检查路径权限（Traverse Permission）**：
Systemd 需要能“穿过”所有父目录到达脚本。
确保 `/srv` 和 `/srv/devs` 目录允许其他人（或 `dev` 组）进入（至少需要 `+x` 权限）：
```bash
ls -ld /srv
ls -ld /srv/devs

```


如果权限看起来像 `drwx------`（只有 owner 能进），而 Systemd 切换的用户如果不是 owner，就会进不去。不过既然你是在 `dev` 用户下操作的，这一步通常没问题。

### 第三步：检查 Runner 安装的用户配置

有时候我们在 `root` 下解压了文件，却尝试用 `dev` 用户运行，或者反过来。

检查一下 Systemd 的配置文件里指定了哪个用户：

```bash
cat /etc/systemd/system/actions.runner.ThatboxAI-backend-docker.thinkbox_self_hosted_runner.service

```

找到 `User=...` 这一行。

* 如果 `User=dev`，那么请确认 `/srv/devs/actions-runner` 目录的所有者确实是 `dev`：
```bash
sudo chown -R dev:devs /srv/devs/actions-runner

```



---

### 总结推荐操作

通常只需要执行**第一步中的第 3 小点（chcon 命令）**即可解决问题。

```bash
# 一条命令修复 SELinux 上下文
sudo chcon -R -t bin_t /srv/devs/actions-runner/

# 再次启动
sudo ./svc.sh start

```
