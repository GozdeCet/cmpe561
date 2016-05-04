# cmpe561


This project trains a HMM POS Tagger by evaluating the transition and emission probabilities according to a training file
and tags a test file by using these probabilities.
It also evaluate the performance of the tagger.

To train the tagger, run the code as :

    python train_hmm_tagger.py training_file.txt --cpostag

this command train the tagger by using cpostag.


To train the tagger by using postag, please run the code :

    python train_hmm_tagger.py training_file.txt --postag

After the training, the code evaluates a 'args.txt' file (to remember the user's preference of cpostag/postag), so for the next steps, 
please be sure that this text file and the next codes are in the same directory.


To tag a test file, run the code as :

    python hmm_tagger.py test_file.txt output_file.txt

This command takes the test_file.txt as an argument and generates an output.



To evaluate the performance of the tagger, run the code as :

    python evaluate_hmm_tagger.py output_file.txt gold.txt

This command takes the output_file.txt from the previous step and a gold.txt and generates 'accuracy_and_confisuon.txt' to compare the output of the tagger with the gold standard for the test data.
In the 'accuracy_and_confisuon.txt' file, you can find the overall accuracy of the tagger, individual accuracy for the each tag and confusion matrix.

