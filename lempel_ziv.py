from random import random
import numpy as np
import math

def generate_seq(prob_table, length):
    #fprob_table is the input probability dictionary
    seq_list = ''
    s = ''
    entropy=0
    while len(seq_list) < 1:
        for k, v in prob_table.items():
            if len(s) == length:
                seq_list = seq_list + s
                s = ''
                break
            rn = random()
            if rn <=  v:
                s += k   
    return seq_list

def calculate_entropy(probabilities):
   return -sum( p * math.log2(p) for p in probabilities)

def parse_data(sequence):
    k=1    
    temp = ''
    for i in sequence:
       if temp in lz_dict.values() or temp == '' :
          temp = temp+i
          continue
       lz_dict[k] = temp
       #print(k, lz_dict[k])
       k +=1
       temp = i
    return lz_dict, k


def find_phrases(num_of_bits):
  temp = {}
  for present_value in lz_dict.values():
    if len(present_value) == 1:
      temp[present_value] = '0'.rjust(num_of_bits, '0') + present_value[0]
    else:
      for past_key, past_value in lz_dict.items():
        if present_value[:len(present_value) - 1] == past_value:
          temp[present_value] = str(bin(past_key).replace("0b", "")).rjust(num_of_bits,'0') + present_value[len(present_value) - 1]
  return temp

def lempel_ziv(sequence):
   lz_dict , count = parse_data(sequence)
   num_bits = math.ceil(math.log2(len(lz_dict.items()))) 
   codewords = find_phrases(num_bits)
   return num_bits, codewords, count


def summarize_info(sequence_lengths,prob_table):
   print("sequence length  \t Nb  \t compression ratio  \t bits per  symbol")
   for length in sequence_lengths:
       sequence = generate_seq(prob_table,length)
       lz_dict = {}
       num_bits, codewords, count= lempel_ziv(sequence)
       seq_bits = (num_bits+8)*count
       compression_ratio = seq_bits / (length*8)
       print(length , " \t\t\t", seq_bits, "\t\t ", compression_ratio,  " \t\t ", seq_bits/length ) 

def summarize_avg(sequence_lengths,prob_table):
   print("sequence length  \t Navg  \t compression ratio  \t bits per  symbol")
   for length in sequence_lengths:
     avg_bits=0
     for i in range (5):
        sequence = generate_seq(prob_table,length)
        lz_dict = {}
        num_bits, codewords, count= lempel_ziv(sequence)
        seq_bits = (num_bits+8)*count
        avg_bits += seq_bits
     avg_bits= avg_bits / 5
     compression_ratio = avg_bits / (length*8)
     print(length , " \t\t\t", seq_bits, "\t\t ", compression_ratio,  " \t\t ", seq_bits/length)


prob_table = {'a': 0.5, 'b': 0.3, 'c': 0.1, 'd': 0.1}
sequence = generate_seq(prob_table,30)
print("sequence is : " ,sequence) 
entropy = calculate_entropy([0.5,0.3,0.1,0.1])
print("source entropy  = ",entropy)
lz_dict = {}
num_bits, codewords, count= lempel_ziv(sequence)
sequence_length= (num_bits+8)*count
print("codewords: ",codewords)
print("number of bits per symbol = ", sequence_length/30)
print("number of bits to encode the sequence = ", sequence_length)
encoded_sequence = ''.join([str(item) for item in codewords.values()])
print("Encoded Sequence: " + encoded_sequence + "\n")

sequence_lengths = {20,50,100,200,400,800,1000,2000}
summarize_info(sequence_lengths,prob_table)
summarize_avg(sequence_lengths,prob_table)
