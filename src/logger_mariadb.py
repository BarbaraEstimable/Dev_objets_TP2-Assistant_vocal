import pymysql


DB_HOST = "localhost"
DB_USER = "iot_sup"
DB_PASSWORD = "iot_sup"
DB_NAME = "iot_supervise"


def journaliser_commande(texte_commande, intention, resultat):
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO commandes_vocales (texte_commande, intention, resultat)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (texte_commande, intention, resultat))
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    journaliser_commande("allume la lampe", "allumer_lampe", "on")
    print("Journalisation OK")