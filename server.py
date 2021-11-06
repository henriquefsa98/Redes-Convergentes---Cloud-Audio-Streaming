# Redes Convergentes - Universidade Federal do ABC

# Professor: Carlos Alberto Kamienski 


# **** Projeto Cloud Streaming de Audio codificado em Ogg Opus!  ****


#  Server, responsavel por codificar um audio bruto em .wav, 
# para um audio .ogg utilizando codec Opus, para uma diminuição 
# de banda de rede utilizada, mantendo a qualidade do audio. 


# Gabriel Batista da Silva, 11047216
# Henrique Fantato, 21053916
# Mikael Alves Monteiro, 21055813


import socket
import threading, pyaudio,pickle,struct, pydub


def audio_stream(host_ip, port, audioPath, audioFormat, audioCodec):
    server_socket = socket.socket()
    server_socket.bind((host_ip, (port-1)))

    server_socket.listen(5)
    CHUNK = 1024
    
    wf = pydub.AudioSegment.from_file(audioPath, format=audioFormat, codec=audioCodec)
    
    p = pyaudio.PyAudio()

    print('server listening at',(host_ip, (port-1)))
   
    stream = p.open(format=p.get_format_from_width(wf.sample_width),
                channels=1,
                rate=wf.frame_rate,
                input=True,
                frames_per_buffer=CHUNK)
             

    client_socket,addr = server_socket.accept()
 
    data = None

    i = 0

    while True:
        if client_socket:
            while True:
              
                data = [wf.get_frame(x) for x in range(i, i+CHUNK)]

                data = [str(s, 'ISO-8859-1') for s in data]
            
                data = ''.join(data)

                data = data.encode('ISO-8859-1')

                a = pickle.dumps(data)

                message = struct.pack("Q",len(a))+a

                client_socket.sendall(message)

                i += CHUNK
                

def audioEncoder(audioPath, originalFormat, desiredPath, desiredFormat, desiredCodec, desiredBitrate):

    audioEntrada = pydub.AudioSegment.from_file(audioPath, format=originalFormat)

    audioEntrada.export(desiredPath, format=desiredFormat,codec=desiredCodec, bitrate=desiredBitrate)

    return desiredPath



def main():

    print("Iniciando Servidor de Streaming de Audio codificado em Ogg Opus! \n")

    audioPath = "audio.wav"

    originalFormat = "wav"

    desiredPath = "audioConvertido.ogg"

    desiredFormat = "ogg"

    desiredCodec = "libopus"

    desiredBitrate = "512k"

    print("Realizando codificacao do audio bruto em .wav para .ogg utilizando codec opus!\n")

    streamingAudioPath = audioEncoder(audioPath, originalFormat, desiredPath, desiredFormat, desiredCodec, desiredBitrate)

    print("Codificaçao concluida!\n")

    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)  # '192.168.1.102'
    print(host_ip)
    port = 9611

    print("Iniciando transmissao do audio via protocolo TCP:")

    t1 = threading.Thread(target=audio_stream, args=(host_ip, port, streamingAudioPath, desiredFormat, desiredCodec))
    t1.start()


if __name__ == "__main__":
    main()