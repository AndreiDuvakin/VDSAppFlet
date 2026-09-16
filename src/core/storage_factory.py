import flet_secure_storage as fss


def create_secure_storage():
    return fss.SecureStorage(
        android_options=fss.AndroidOptions(
            reset_on_error=True,
            enforce_biometrics=False,
            migrate_on_algorithm_change=True,
            key_cipher_algorithm=fss.KeyCipherAlgorithm.AES_GCM_NO_PADDING,
            storage_cipher_algorithm=fss.StorageCipherAlgorithm.AES_GCM_NO_PADDING,
        ),
    )
