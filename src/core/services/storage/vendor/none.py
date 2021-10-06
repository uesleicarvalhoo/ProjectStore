from typing import Union

from .. import Storage


class NoneStorage(Storage):
    """
    Storage que não executa nada, apenas implementa os metódos sem nenhuma ação
    conforme o design pattern: https://sourcemaking.com/design_patterns/null_object
    """

    def upload_file(self, file: Union[str, bytes], key: str, bucket: str = None) -> str:
        pass

    def check_file_exists(self, key: str, bucket: str = None) -> bool:
        return True

    def delete_file(self, key: str, bucket: str = None) -> None:
        pass
