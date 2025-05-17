import xml.etree.ElementTree as ET


def parse_sts_credentials(xml_str: str) -> dict:
    """
    Парсит XML-ответ от MinIO STS и возвращает словарь с полями,
    подходящими под STSCredentialsSerializer.
    """
    # Пространство имён из вашего XML
    ns = {"sts": "https://sts.amazonaws.com/doc/2011-06-15/"}

    root = ET.fromstring(xml_str)
    creds = root.find(".//sts:Credentials", ns)
    if creds is None:
        raise ValueError("Credentials element not found in XML")

    return {
        "access_key_id": creds.find("sts:AccessKeyId", ns).text,  # type: ignore
        "secret_access_key": creds.find("sts:SecretAccessKey", ns).text,  # type: ignore
        "session_token": creds.find("sts:SessionToken", ns).text,  # type: ignore
    }
