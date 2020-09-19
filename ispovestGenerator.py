import gpt_2_simple as gpt2
import os
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

start = time.process_time()

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')
text = gpt2.generate(sess,
                     length=256,
                     temperature=0.7,
                     nsamples=10,
                     batch_size=1,
                     top_k=40,
                     truncate='\n'
                     )

print(text)
print(time.process_time() - start)
