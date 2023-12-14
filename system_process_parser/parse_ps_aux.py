from datetime import datetime
from subprocess import run, PIPE


class UsersProcesses:

    def __init__(self):
        self.stdout = self.ps_aux_stdout()
        self.users = self.get_users()
        self.users_process = self.get_user_process()
        self.memory = self.get_memory()
        self.max_memory_process = self.get_max_memory_process()
        self.cpu = self.get_cpu()
        self.max_cpu_process = self.get_max_cpu_process()

    """ Get ps aux stdout in utf-8 format """

    def ps_aux_stdout(self):
        return run(["ps", "aux"], stdout=PIPE, encoding='utf-8').stdout.split("\n")

    """ Get non empty users """

    def get_users(self):
        return set(user.split()[0] for user in self.stdout
                   if user.strip() and "USER" not in user)

    """ Get for every users information with non empty processes
     with assertion that process equal user """

    def get_user_process(self):
        user_process = {}
        for user in self.users:
            user_process[user] = [process for process in self.stdout
                                  if process.strip() and "USER" not in process
                                  and process.split()[0] == user]
        return user_process

    """ Get used memory information """

    def get_memory(self):
        return [round(float(memory.split()[3])) for memory in self.stdout
                if memory.strip() and "MEM" not in memory]

    """ Get max memory process used information """

    def get_max_memory_process(self):
        max_memory_process = ("", "", 0.0)
        for user, processes in self.users_process.items():
            for process in processes:
                memory = float(process.split()[3])
                if memory > max_memory_process[2]:
                    process_name = process.split()[10]
                    if len(process_name) > 20:
                        process_name = process_name[:20]
                    max_memory_process = (user, process_name, memory)
        return max_memory_process

    """ Get used CPU information """

    def get_cpu(self):
        return [round(float(cpu.split()[2])) for cpu in self.stdout
                if cpu.strip() and "CPU" not in cpu]

    """ Get max CPU process used information """

    def get_max_cpu_process(self):
        max_cpu_process = ("", "", 0.0)
        for user, processes in self.users_process.items():
            for process in processes:
                cpu = float(process.split()[2])
                if cpu > max_cpu_process[2]:
                    process_name = process.split()[10]
                    if len(process_name) > 20:
                        process_name = process_name[:20]
                    max_cpu_process = (user, process_name, cpu)
        return max_cpu_process

    def system_status(self, file):
        print(f"System status report:\n"
              f"    System users: {', '.join(self.users)}\n"
              f"    Total numbers of users: {len(self.users)}\n"
              f"    User process:",
              file=file
              )
        for user, processes in self.users_process.items():
            print(f"        User {user}: {len(processes)}",
                  file=file
                  )
        print(f"    Memory used: {sum(self.memory)} mb\n",
              f"   CPU used: {sum(self.cpu)} %\n",
              f"   Max memory process used: {str(self.max_memory_process).replace('(', '').replace(')', '')} mb\n",
              f"   Max CPU process used: {str(self.max_cpu_process).replace('(', '').replace(')', '')} %",
              file=file)


if __name__ == "__main__":
    users_process = UsersProcesses()
    current_date_and_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(f"System process information {current_date_and_time}.txt", "w") as file:
        users_process.system_status(file)
