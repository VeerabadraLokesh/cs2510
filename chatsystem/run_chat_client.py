
from __future__ import print_function

import logging
import uuid
import grpc
import chat_system_pb2
import chat_system_pb2_grpc
from time import sleep
from google.protobuf.json_format import MessageToJson
from datetime import datetime
import json
import threading
from threading import Thread
from queue import Queue
from client import constants as C
from client.display_manager import display_manager

global state


# print(dir(dict))
class ClientState():
    def __init__(self, initial={}):
        self._lock = threading.Lock()
        self._state = initial

    def __setitem__(self, key, value):
        with self._lock:
            self._state[key] = value

    def __getitem__(self, key):
        return self._state[key]

    def __contains__(self, key):
        print(key, self._state)
        return (key in self._state)

    def __str__(self) -> str:
        return self._state.__str__()

    def get(self, key):
        return self._state.get(key)
    
    def get_dict(self):
        return self._state


state = ClientState()

# state['a'] = 'b'
# with open('/tmp/test.json1', 'w') as wf:
#     json.dump(state.get_dict(), wf)


def check_state(check_point):
    if check_point > C.SERVER_CONNECTION_CHECK:
        if not state.get(C.SERVER_ONLINE):
            raise Exception(C.NO_ACTIVE_SERVER)
    if check_point > C.USER_LOGIN_CHECK:
        if state.get(C.ACTIVE_USER_KEY) is None:
            raise Exception(C.NO_ACTIVE_USER)
    if check_point > C.JOIN_GROUP_CHECK:
        if state.get(C.ACTIVE_GROUP_KEY) is None:
            raise Exception(C.NO_ACTIVE_GROUP)


def exit_group(user_id, group_id):
    stub=state.get(C.STUB)
    stub.ExitGroup(chat_system_pb2.Group(
        group_id=group_id, user_id=user_id))
    display_manager.info(
        f"{user_id} successfully exited group {group_id}")
    state[C.ACTIVE_GROUP_KEY] = None


def logout_user(user_id):
    stub=state.get(C.STUB)
    if state.get(C.ACTIVE_USER_KEY) == user_id:
        exit_group(user_id=user_id,
                    group_id=state[C.ACTIVE_GROUP_KEY])

        stub.LogoutUser(chat_system_pb2.User(user_id=user_id))
        display_manager.info(f"Logout successful for user_id {user_id}")
        state[C.ACTIVE_USER_KEY] = None


def close_connection(stub=None, channel=None):
    """
    manages 3 exit cases
    channel: 
    1st case: 
    changing group or changing user
    
    """
    user_id = state.get(C.ACTIVE_USER_KEY)
    if user_id is not None:
        logout_user(user_id)
    channel.close()
    display_manager.info(
        f"terminated {state[C.SERVER_CONNECTION_STRING]} successfully")
    state[C.ACTIVE_CHANNEL] = None
    state[C.SERVER_ONLINE] = False
    state[C.SERVER_CONNECTION_STRING] = None
    state[C.STUB] = None


def health_check():
    while True:
        try:
            stub = state.get(C.STUB)
            if stub is not None:
                server_status = stub.HealthCheck(
                    chat_system_pb2.BlankMessage())
                if server_status.status is True:
                    state[C.SERVER_ONLINE] = True
                else:
                    # print("enter", "server_status.status ", server_status.status )
                    state[C.SERVER_ONLINE] = False
            else:
                state[C.SERVER_ONLINE] = False
        except Exception as ex:
            state[C.SERVER_ONLINE] = False
            display_manager.warn('server disconnected')
        sleep(C.HEALTH_CHECK_INTERVAL)


def get_messages():
    while True:
        stub = state.get(C.STUB)
        if stub is None:
            state[C.SERVER_ONLINE] = False
        else:
            messages = stub.GetMessages(chat_system_pb2.Group(group_id = state.get(C.ACTIVE_GROUP_KEY)))
            for message in messages:
                state[C.MESSAGE_NUMBER] += 1
                state[C.MESSAGE_ID_TO_NUMBER_MAP][message.message_id] =  state[C.MESSAGE_NUMBER]
                state[C.MESSAGE_NUMBER_TO_ID_MAP][state[C.MESSAGE_NUMBER]] = message.message_id
                print(f"{state[C.MESSAGE_ID_TO_NUMBER_MAP][message.message_id]}. {messages.user_id}: {message.text}")
        
        sleep(C.MESSAGE_CHECK_INTERVAL)


def join_server(server_string):
    if server_string == state.get(C.SERVER_CONNECTION_STRING):
        display_manager.info(f'Already connected to server {server_string}')
        return state.get(C.STUB)
    channel = state.get(C.ACTIVE_CHANNEL)
    if channel:
        close_connection(channel)
    display_manager.info(f"Trying to connect to server: {server_string}")
    channel = grpc.insecure_channel(server_string)
    stub = chat_system_pb2_grpc.ChatServerStub(channel)
    server_status = stub.HealthCheck(chat_system_pb2.BlankMessage())
    if server_status.status is True:
        display_manager.info("Server connection active")
        state[C.ACTIVE_CHANNEL] = channel
        state[C.SERVER_ONLINE] = True
        state[C.SERVER_CONNECTION_STRING] = server_string
        state[C.STUB] = stub
    return stub


def get_user_connection(stub, user_id):
    try:
        check_state(C.USER_LOGIN_CHECK)
        if state.get(C.ACTIVE_USER_KEY) is not None:
            if state.get(C.ACTIVE_USER_KEY) != user_id:
                logout_user(stub, user_id=state[C.ACTIVE_USER_KEY])
            else:
                display_manager.info(f"User {user_id} already logged in")
                return
        status = stub.GetUser(chat_system_pb2.User(user_id=user_id))
        if status.status is True:
            display_manager.info(f"Login successful with user_id {user_id}")
            state[C.ACTIVE_USER_KEY] = user_id
        else:
            raise Exception("Login not successful")
    except grpc.RpcError as rpcError:
        raise rpcError
    except Exception as ex:
        raise ex


def enter_group_chat(stub, group_id):
    try:
        check_state(C.JOIN_GROUP_CHECK)
        current_group_id = state.get(C.ACTIVE_GROUP_KEY)
        user_id = state.get(C.ACTIVE_USER_KEY)
        if current_group_id is not None and current_group_id != group_id:
            exit_group(user_id=user_id, group_id=current_group_id)
        elif current_group_id == group_id:
            display_manager.info(f"User {user_id} already in group {group_id}")
            return
        group_details = stub.GetGroup(
            chat_system_pb2.Group(group_id=group_id, user_id=user_id))
        group_data = MessageToJson(group_details)
        if group_details.status is True:
            display_manager.info(f"Successfully joined group {group_id}")
            state[C.ACTIVE_GROUP_KEY] = group_id
            state[C.GROUP_DATA] = group_data
            state[C.MESSAGE_ID_TO_NUMBER_MAP] = {}
            state[C.MESSAGE_NUMBER] = 0
            state[C.MESSAGE_NUMBER_TO_ID_MAP] = {}
            state[C.MESSAGES] = {}
        else:
            raise Exception("Entering group not successful")
    except Exception as ex:
        print(f"Error: {ex}. Please try again.")
        raise ex


def get_timestamp() -> int:
    """
    returns UTC timestamp in microseconds
    """
    return int(datetime.now().timestamp() * 1_000_000)


def get_unique_id() -> str:
    """
    returns unique string generated by MD5 hash
    """
    return str(uuid.uuid4())


def build_message(message_text, message_number, message_type):
    
    if message_type == C.APPEND_TO_CHAT_COMMANDS[0]:
        message_id = state[C.MESSAGE_NUMBER_TO_ID_MAP][message_number]
        state[C.MESSAGES][message_id].text = [message_text]
        message = state[C.MESSAGES][message_id]
        message.message_type = message_type

    elif message_type == C.LIKE_COMMANDS[0]:
        message_id = state[C.MESSAGE_NUMBER_TO_ID_MAP][message_number]
        state[C.MESSAGES][message_id].likes = {state[C.ACTIVE_USER_KEY]: 1}
        message = state[C.MESSAGES][message_id]
        message.message_type = message_type

    elif message_type == C.UNLIKE_COMMANDS[0]:
        message_id = state[C.MESSAGE_NUMBER_TO_ID_MAP][message_number]
        state[C.MESSAGES][message_id].likes = {state[C.ACTIVE_USER_KEY]: 0}
        message = state[C.MESSAGES][message_id]
        message.message_type = message_type

    else:
        message_id=get_unique_id()

        message = chat_system_pb2.Message(
            group_id=state.get(C.ACTIVE_GROUP_KEY),
            user_id=state.get(C.ACTIVE_USER_KEY),
            creation_time=get_timestamp(),
            text=[message_text],
            message_id=message_id,
            likes={state.get(C.ACTIVE_USER_KEY): 0},
            message_type=C.NEW
        )
    state[C.MESSAGES][message_id] = message

    return message


def post_message(message_text: str, post_message_queue: Queue, post_message_event: threading.Event, message_number, message_type):
    try:
        check_state(C.SENT_MESSAGE_CHECK)
        message = build_message(message_text, message_number, message_type)
        post_message_queue.put(message)
        post_message_event.set()
    except Exception as ex:
        raise ex


def send_messages(post_message_queue, post_message_event):
    while True:
        post_message_event.wait()  # sleeps till post_message_event.set() is called
        stub = state[C.STUB]
        while post_message_queue.qsize():
            message = post_message_queue.queue[0]
            retry = 3
            while retry > 0:
                try:
                    print("message", message)
                    status = stub.PostMessage(message)
                    if status.status is True:
                        display_manager.info("Message sent successfuly")
                        post_message_queue.get()

                    else:
                        logging.error(
                            f"Message sending failed. Response from server: {status.statusMessage}")
                    retry = 0
                    break
                except grpc.RpcError as rpcError:
                    retry -= 1
                    if retry == 0:
                        logging.error(
                            f"Message sending failed. Error: {rpcError}") 
            break
        post_message_event.clear()


def run():
    status = None
    stub = None

    health_check_thread = Thread(target=health_check, daemon=True)
    health_check_thread.start()

    # retry queue that stores users' messages that will get delivered
    # even if message fails to be sent to server
    post_message_queue = Queue()
    post_message_event = threading.Event()
    send_message_thread = Thread(target=send_messages, args=[post_message_queue, post_message_event], daemon=True)
    send_message_thread.start()

    get_message_thread = Thread(target=get_messages, daemon=True)
    get_message_thread.start()
    print("Client started")
    while True:
        # display_manager.write("hello", "world")
        user_input = display_manager.read()
        if ' ' in user_input:
            command = user_input.split(' ')[0].strip()
        else:
            command = user_input
        # try:
        group_id = ''
        # connect mode : c
        if command in C.CONNECTION_COMMANDS:
            server_string = user_input[2:].strip()
            if server_string == '':
                server_string = C.DEFAULT_SERVER_CONNECTION_STRING
            stub = join_server(server_string)
        # exit mode: q 
        elif command in C.EXIT_APP_COMMANDS:
            close_connection(channel=state.get(C.ACTIVE_CHANNEL))
            break
        # login user mode: u
        elif command in C.LOGIN_COMMANDS:
            user_id = user_input[2:].strip()
            if len(user_id) < 1:
                raise Exception("Invalid user_id")
            get_user_connection(stub, user_id)
        # join group mode: j
        elif command in C.JOIN_GROUP_COMMANDS:
            group_id = user_input[2:].strip()
            if len(group_id) < 1:
                raise Exception("Invalide group_id")
            enter_group_chat(stub, group_id)
        
        # like mode: l
        elif command in C.LIKE_COMMANDS or command in C.UNLIKE_COMMANDS:
            splits = user_input.split(" ")
            message_number = splits[1]
            if not message_number.isdigit():
                raise Exception("Invalid command")
            message_number = int(message_number)
            post_message(None, post_message_queue, post_message_event, message_number, message_type=command)

        # append mode: a
        elif command in C.APPEND_TO_CHAT_COMMANDS:
            splits = user_input.split(" ")
            message_number = splits[1]
            message_text = " ".join(splits[2:])
            if not message_number.isdigit():
                raise Exception("Invalid command")
            message_number = int(message_number)
            post_message(message_text, post_message_queue, post_message_event, message_number, message_type=command)

        # like mode: l
        elif command in C.LIKE_COMMANDS:
            message_number = user_input.split(" ")[1]
            if not message_number.isdigit():
                raise Exception("Invalid command")
            message_number = int(message_number)
            post_message(
                message_text=None,
                post_message_queue=post_message_queue, 
                post_message_event=post_message_event, 
                message_number=message_number, 
                message_type=command
                )

        # typing mode & also implement get messages mode
        else:
            message_text = user_input
            post_message(message_text, post_message_queue, post_message_event, None, message_type=C.NEW)
        # except grpc.RpcError as rpcError:
        #     logging.error(f"grpc exception: {rpcError}")
        # except Exception as e:
        #     logging.error(
        #         f"Error: {e}")


if __name__ == "__main__":
    
    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%d-%m-%Y:%H:%M:%S',
                        level=logging.INFO)
    run()
