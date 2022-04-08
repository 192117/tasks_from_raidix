from setuptools import setup, find_packages

setup(
    name='chat',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    author="Kalimullin Artur",
    author_email="noti1996@gmail.com",
    description="This is a simple client/server chat with asyncio and threading.",
    url='https://github.com/192117/tasks_from_raidix',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'server = chat.server:run_server',
            'client = chat.chatclient:main',
            ]
        }
)
