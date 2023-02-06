# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_system_pb2 as chat__system__pb2


class ChatServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUser = channel.unary_unary(
                '/chatsystem.ChatServer/GetUser',
                request_serializer=chat__system__pb2.User.SerializeToString,
                response_deserializer=chat__system__pb2.Status.FromString,
                )
        self.GetGroup = channel.unary_unary(
                '/chatsystem.ChatServer/GetGroup',
                request_serializer=chat__system__pb2.Group.SerializeToString,
                response_deserializer=chat__system__pb2.GroupDetails.FromString,
                )
        self.GetMessages = channel.unary_stream(
                '/chatsystem.ChatServer/GetMessages',
                request_serializer=chat__system__pb2.Group.SerializeToString,
                response_deserializer=chat__system__pb2.Message.FromString,
                )
        self.PostMessage = channel.unary_unary(
                '/chatsystem.ChatServer/PostMessage',
                request_serializer=chat__system__pb2.Message.SerializeToString,
                response_deserializer=chat__system__pb2.Status.FromString,
                )


class ChatServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PostMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=chat__system__pb2.User.FromString,
                    response_serializer=chat__system__pb2.Status.SerializeToString,
            ),
            'GetGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGroup,
                    request_deserializer=chat__system__pb2.Group.FromString,
                    response_serializer=chat__system__pb2.GroupDetails.SerializeToString,
            ),
            'GetMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMessages,
                    request_deserializer=chat__system__pb2.Group.FromString,
                    response_serializer=chat__system__pb2.Message.SerializeToString,
            ),
            'PostMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.PostMessage,
                    request_deserializer=chat__system__pb2.Message.FromString,
                    response_serializer=chat__system__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chatsystem.ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chatsystem.ChatServer/GetUser',
            chat__system__pb2.User.SerializeToString,
            chat__system__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chatsystem.ChatServer/GetGroup',
            chat__system__pb2.Group.SerializeToString,
            chat__system__pb2.GroupDetails.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chatsystem.ChatServer/GetMessages',
            chat__system__pb2.Group.SerializeToString,
            chat__system__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PostMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chatsystem.ChatServer/PostMessage',
            chat__system__pb2.Message.SerializeToString,
            chat__system__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
