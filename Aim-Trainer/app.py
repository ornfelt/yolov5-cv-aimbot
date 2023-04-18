from classes.App import App
from PIL.ImageColor import getrgb
import json

def setConfig():
    """
    Function to create or receive program settings by a .json file.
    """

    filename = "config.json"
    indent = 4

    # Dicionário com as configurações padrões do programa.
    default_config = {

        "Colors":{
            "Final_scoreboard_background_color":App.FINAL_SCOREBOARD_BACKGROUND_COLOR,
            "Scoreboard_color":App.SCOREBOARD_COLOR,
            "Target_colors":App.TARGET_COLORS,
            "Target_area_colors":App.TARGET_AREA_COLORS
            },

        "Extra difficulty settings":{
            "Lives":App.LIVES,
            "Missing_shots_decreases_life":App.MISSING_SHOTS_DECREASES_LIFE,
            },

        "Performance":{
            "Frames_per_second":App.FRAMES_PER_SECOND,
            "Sounds_buffer":App.SOUNDS_BUFFER
            },

        "Targets":{
            "Target_limit_per_second":App.TARGET_LIMIT_PER_SECOND,
            "Target_radius":App.TARGET_RADIUS,
            "Targets_per_second":App.TARGETS_PER_SECOND,
            "Target_speed":App.TARGET_SPEED
        },
        
    }

    # Cria um dicionário com as configurações padrões para ser modificado
    file_config = default_config.copy()

    try:
        file = open(filename)
        config = json.loads(file.read())    
        file.close()
        
        for mainKey in config.keys():

            # Verifica se a chave principal é permitida
            if not mainKey in default_config.keys():
                continue

            for key in config[mainKey].keys():

                # Verifica se a chave é permitida
                if not key in default_config[mainKey].keys():
                    continue
                
                if "color" in key.lower():
                    
                    if "colors" in key.lower():
                        colors_list = []
                    
                        # Troca o nome das cores por tuplas em RGB
                        try:
                            for color in config[mainKey][key]:
                                if type(color) is str:
                                    color = getrgb(color)
                                elif type(color) in [tuple,list]: 
                                    color = color
                                else: raise TypeError
                                colors_list.append(color)
                            file_config[mainKey][key] = colors_list.copy()
                        except: pass
                        continue

                    # Troca o nome da cor por uma tupla em RGB
                    try:
                        color = config[mainKey][key]
                        if type(color) is str:
                            color = getrgb(color)
                        elif type(color) in [tuple,list]: 
                            color = color
                        else: raise TypeError
                        file_config[mainKey][key] = color
                    except: 
                        continue
                
                # Coloca a configuração do arquivo no dicionário
                file_config[mainKey][key] = config[mainKey][key]
        
        # Passa os valores do dicionário para a classe principal do programa como atributo
        for mainKey in file_config.keys():
            for key in file_config[mainKey].keys():
                setattr(App,key.upper(),file_config[mainKey][key])
                    
    except:
        file = open(filename,"w")
        file.write(json.dumps(default_config,indent=indent))
        file.close()


if __name__ == "__main__":
    setConfig()
    App().run()
