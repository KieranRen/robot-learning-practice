# M0 Environment Verification

## Context

- Date
- Knowledge repository URL
- Knowledge tag or unreleased status
- Knowledge commit, full SHA
- Work repository URL or non-private identifier
- Work commit, full SHA
- Uncommitted changes, if any
- Related Issue or personal progress entry
- Operating system
- Shell

个人报告默认放在个人学习仓库。知识库来源版本与实际运行代码的提交都要记录，代码有未提交修改时说明修改范围。请只保留排查兼容性所需的信息，删除主机名、用户名、私人路径、IP 地址和凭据。公开报告时只引用读者有权限访问且适合公开的信息。

## Environment

- Conda version
- Environment name used for this run
- Python version
- NumPy version
- pytest version

## Commands and results

```bash
python examples/hello_robot.py
python -m pytest
```

记录每条命令成功或失败，并给出必要的输出摘要。不要把尚未执行的命令标记为通过。

## Problems and resolution

写明最短复现步骤、错误摘要、已经尝试的检查和最终状态。没有问题时写 `None observed`。

## Privacy check

- [ ] 没有主机名、用户名或学号
- [ ] 没有私人绝对路径或 IP 地址
- [ ] 没有令牌、密码或其他凭据
- [ ] 结果来自实际运行
