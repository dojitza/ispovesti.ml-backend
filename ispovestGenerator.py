import gpt_2_simple as gpt2
import os
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')


def generateIspovest(prefix):
    text = gpt2.generate(sess,
                         length=256,
                         prefix=prefix,
                         temperature=0.7,
                         nsamples=1,
                         batch_size=1,
                         top_k=40,
                         truncate='\n',
                         return_as_list=True
                         )
    return text[0]
