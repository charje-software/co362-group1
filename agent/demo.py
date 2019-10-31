import threading

from oracle import Oracle
from agent import Agent

PERIOD_LENGTH = 15
ROUNDS = 10
ACCOUNTS = ['0x35392caED05CB4A7AE79540530E2AD2a083B536A',
            '0x7d6ccA0864F4c0b5FeDEb70f3d7c8b4d50EF7cD8',
            '0xe3fc73f3Cfd6C9a8d4fe8dae3736AF15fFd7299F',
            '0x5e461a87DD275D898170042b2508C17b160635f6',
            '0x08B8ED3867370E0FF7379b1Ab13E0ab5fFdD457d',
            '0x8C97d51c9220d335380239737f67265D5cb6C45A',
            '0x67BCB327244E855fD179837bBA7510b2eaf80F41',
            '0x65ce6E98f733b5Ccb7d9D20f7cd919ce7dcCdd5F',
            '0x8b3A2AcA817beebafA45f28340c70cDaB5D02e16']

agents = [Agent(a) for a in ACCOUNTS]
oracle = Oracle()

try:
    threads = [threading.Thread(target=oracle.run, args=(PERIOD_LENGTH, ROUNDS))] + \
         [threading.Thread(target=agent.run, args=(PERIOD_LENGTH, ROUNDS)) for agent in agents]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    print("Stopping simulation..")
