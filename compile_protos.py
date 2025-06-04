import subprocess
import os

def compile_protos():
    proto_dir = os.path.join(os.path.dirname(__file__), 'protos')
    
    if not os.path.exists(proto_dir):
        os.makedirs(proto_dir)
    
    subprocess.run([
        'python', '-m', 'grpc_tools.protoc',
        f'--proto_path={proto_dir}',
        f'--python_out={proto_dir}',
        f'--grpc_python_out={proto_dir}',
        os.path.join(proto_dir, 'chat.proto')
    ])

if __name__ == '__main__':
    compile_protos()
