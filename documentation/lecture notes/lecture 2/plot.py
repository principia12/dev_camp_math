import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np
import math
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api


def basic_fft_example():
    Fs = 300.0;  # sampling rate
    Ts = 1.0/Fs; # sampling interval
    t = np.arange(0,1,Ts) # time vector

    #ff = 5;   # frequency of the signal
    #y = np.sin(2*np.pi*5*t)
    y = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*10*t)

    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n//2)] # one side frequency range

    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(n//2)]

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(t,y)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
    ax[1].set_xlabel('Freq (Hz)')
    ax[1].set_ylabel('|Y(freq)|')

    plot_url = py.plot_mpl(fig, filename='mpl-basic-fft')
    print(plot_url)
    
def basic_fft(freq0, freq1):
    Fs = 300.0;  # sampling rate
    Ts = 1.0/Fs; # sampling interval
    t = np.arange(0,1,Ts) # time vector

    #ff = 5;   # frequency of the signal
    #y = np.sin(2*np.pi*5*t)
    y = np.sin(2*np.pi*freq0*t) + np.sin(2*np.pi*freq1*t)

    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n//2)] # one side frequency range

    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(n//2)]

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(t,y)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
    ax[1].set_xlabel('Freq (Hz)')
    ax[1].set_ylabel('|Y(freq)|')

    plot_url = py.plot_mpl(fig, filename='mpl-basic-fft')
    

def modulation(freq0, freq1, signal, sample_rate = 300, quiet = True):
    ''' signal is a list of 0 or 1. 
    freq0, freq1 represents frequency to decode 0 or 1, respectively. 
    step is time step for each signal. 
    
    modulation returns concatanation of sine functions accordingly. 
    '''
    print('modulation using 0:%d, 1:%d'%(freq0, freq1))
    Fs = sample_rate
    Ts = 1.0/Fs
    t = []
    y = []
    
    for i in range(len(signal)):
        tmp = np.arange(i, i+1, Ts)
        t.extend(tmp)
        if signal[i] == 0:
            y.extend(np.sin(2*np.pi*freq0*tmp))
        elif signal[i] == 1:
            y.extend(np.sin(2*np.pi*freq1*tmp))
        else:
            assert False, 'Signal should be 0 or 1, %d found'%(singal[i])
            
    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n//2)] # one side frequency range

    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(n//2)]
    if not quiet:
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(t,y)
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Amplitude')
        ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
        ax[1].set_xlabel('Freq (Hz)')
        ax[1].set_ylabel('|Y(freq)|')

        plot_url = py.plot_mpl(fig, filename='mpl-basic-fft')
    
    return y, t
            
            
    
def create_signal(signals, client_window_width = 2, sample_rate = 300,):
    ''' signals is a list of 2-tuple that contains (client_id, signal_list). 
    client_id is an integer representing client's id. 
    signal_list is a list of 0 or 1 representing the signal that client is expected to recieve. 
    '''
    w = client_window_width
    y = [0] * (len(list(signals)[0][1] * sample_rate))
    t = []
    for c_id, sig in signals:
        #y, t = modulation(c_id*2, c_id*2+1, sig)
        #print(len(y), len(t))
        y = [e+f for e,f in zip(y, modulation(c_id*w+1, c_id*w+3, sig)[0])]
        t = [e for e in modulation(c_id*w+1, c_id*w+3, sig)[1]]
    plt.plot(t, y)
    plt.savefig('img/signal.png')
    
    return y, t
    
    
def decode_signal(signal, time_interval, client_id = None, 
            client_num = 0, sample_rate = 300, 
            client_window_width = 2, quiet = True,):
    ''' Given a signal, decode it accordingly. 
    '''
    Fs = sample_rate
    Ts = 1.0/Fs
    w = client_window_width
    res = []
    w_size = (client_num+1)*w
    client_vec = [0] * w_size
    if client_id is not None:
        x = (w-1)//2 +1 
        client_vec[client_id*w+x] = 1
        #print('client vector for client %d'%client_id, client_vec)
    for i in range(len(signal)//sample_rate): # length of original signal
        y = signal[i*sample_rate:(i+1)*sample_rate]
        n = len(y) # length of the signal
        k = np.arange(n)
        T = n/Fs
        t = time_interval[i*sample_rate:(i+1)*sample_rate]
        frq = k/T # two sides frequency range
        frq = frq[range(n//2)] # one side frequency range

        Y = np.fft.fft(y)/n # fft computing and normalization
        Y = Y[range(n//2)]
        if not quiet:
            fig, ax = plt.subplots(2, 1)
            ax[0].plot(t,y)
            ax[0].set_xlabel('Time')
            ax[0].set_ylabel('Amplitude')
            ax[1].plot(frq,abs(Y), 'r') # plotting the spectrum
            ax[1].set_xlabel('Freq (Hz)')
            ax[1].set_ylabel('|Y(freq)|')
            #plot_url = py.plot_mpl(fig, filename='mpl-basic-fft')    
            if client_id is None:
                plt.savefig('img/%d.png'%i)
            else:   
                import os
                if not os.path.exists('img/client%d'%client_id):
                    os.makedirs('img/client%d'%client_id)

                plt.savefig('img/client%d/%d.png'%(client_id, i))
                plt.close('all')
        if client_id is None:
            v = maxarg(frq, abs(Y), len(signal)//sample_rate + 1)
            u = [0,0,0,0,0,0,0,0,0,0,1]
            res.append(inner_product(v,u))
            print(i, inner_product(v,u))
        #print(inner_product(maxarg(frq, abs(Y), w_size), client_vec))
        else:
            v = maxarg(frq, abs(Y), w_size)
            u = client_vec
            #print(u)
            #print(v)
            #print(i, inner_product(v,u))
            res.append(inner_product(v,u))
    return res
    #return bin2string(res)
def check_error_rate():
    pass


# encoding-decoding function 
    
def dec2bin(num):
    res = [int(c) for c in bin(num).lstrip('0b')]
    
    return [0]*(5-len(res)) + res
    

def bin2dec(lst):
    return sum([2**(4-idx)*elem for idx, elem in enumerate(lst)])

def alpha2bin(char):
    alphabet = 'abcdefghijklmnopqrstuwxyz '
    ind = alphabet.index(char.lower())
    
    return dec2bin(ind)
    
def bin2alpha(lst):
    alphabet = 'abcdefghijklmnopqrstuwxyz '
    return alphabet[bin2dec(lst)]
    
def string2bin(text, max_length = 1,):
    res = []
    
    for c in text:
        res.extend(alpha2bin(c))
    
    for i in range(max_length-len(text)):
        res.extend(alpha2bin(' '))
    
    return res
    
def bin2string(lst):
    assert len(lst)%5 == 0
    res = ''
    for i in range(len(lst)//5):
        res += bin2alpha(lst[5*i:5*i+5])
    return res
    
# function for getting local maxarg of signal 
def maxarg(frq, signal, window_size):
    res = []
    for idx, elem in enumerate(signal):
        if idx == 0 or idx == len(signal)-1:
            pass
        elif 10*signal[idx-1] < elem and elem > 10*signal[idx+1]:
            res.append(round(frq[idx]))
    
    tmp = [0] * window_size
    for elem in res:
        try:
            tmp[int(elem)] = 1
        except IndexError:
            pass
            #print('Not used frequency %d observed'%(elem))
            
    return tmp
       
def inner_product(l,r):
    assert len(l) == len(r)
    return sum([x*y for x,y in zip(l,r)])
       
if __name__ == '__main__':
    #basic_fft_example()
    
    # alphabet decoding/encoding test
    '''
    alphabet = 'abcdefghijklmnopqrstuwxyz '
    tmp = []
    for c in alphabet:
        print(alpha2bin(c))
        tmp.append(alpha2bin(c))
        
    for t in tmp:
        print(bin2alpha(t))
        
    print(bin2string(string2bin(alphabet)))
    print(alphabet)
    '''
    
    # simple modulation test - single client 
    alphabet = 'abcdefghijklmnopqrstuwxyz '
    res = decode_signal(*modulation(5, 10, string2bin('hi'), quiet = False), quiet = False)
    print(res)
    print(bin2string(res))
    
    '''
    # sending signals to multiple clients
    alphabet = 'abcdefghijklmnopqrstuwxyz '
    client_list = list(range(1,10))
    signal_list = [string2bin(alphabet[x], max_length = 10) \
                            for x in client_list]
    
    max_len = 20
    signal_list = [\
        string2bin('hello world', max_length = max_len),
        string2bin('hello there', max_length = max_len),
        string2bin('who are you', max_length = max_len),
        string2bin('ill be back', max_length = max_len),
        string2bin('goodbye', max_length = max_len),
        string2bin('cs stud', max_length = max_len),
        string2bin('nothing', max_length = max_len),
        string2bin('null', max_length = max_len),
        string2bin('Nonedfdf', max_length = max_len),]
    
    signals = [(x,y) for x,y in zip(client_list, signal_list)]
    
    y, t = create_signal(signals, client_window_width = 5)
    for i in client_list:
        print('client id %d decoding signal'%i)
        res = decode_signal(y, t, client_id = i, client_window_width = 5, 
                    client_num = len(client_list), quiet = True)
        print('decoded signal : %s'%bin2string(res))
    '''
    
    
    