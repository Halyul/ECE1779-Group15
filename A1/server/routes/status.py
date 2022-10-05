def status():
    return True, 200, dict(
        status=[
            { "name": "Snow", "value": "Jon" },
            { "name": "Lannister", "value": "Cersei" },
            { "name": "Lannister", "value": "Jaime" },
            { "name": "Stark", "value": "Arya" },
            { "name": "Targaryen", "value": "Daenerys" },
            { "name": "Melisandre", "value": None },
            { "name": "Clifford", "value": "Ferrara" },
            { "name": "Frances", "value": "Rossini" },
            { "name": "Roxie", "value": "Harvey" },
        ]
    )
