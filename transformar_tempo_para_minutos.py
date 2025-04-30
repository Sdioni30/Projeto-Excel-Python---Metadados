def tempo_audio_em_minutos(segundos):
    segundos = int(segundos)
    if segundos:  
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        return f'{horas:02}:{minutos:02}:{segundos:02}'
    return "00:00:00"