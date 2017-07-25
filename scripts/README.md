# How to run
- concat_head_rotate.py:
    ```sh
    $ python concat_head_rotate.py [directory of IEMOCAP_full_release]
    ```

- extract_emotion.py
    ```sh
    $ python extract_emotion.py [directory of IEMOCAP_full_release]
    ```

- extract_phoneme.py
    ```sh
    $ python extract_phoneme.py [directory of IEMOCAP_full_release]
    ```
Above three scripts will create a folder 'IEMOCAP_train_data' into your current directory.


- filter.py
    ```sh
    $ python filter.py [file or directory .dat file] [phoneme] [emotion]
    ```
