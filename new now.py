import networkx as nw #グラフを表示させるのに必要なライブラリ
import math
import folium
import os
import json

# Flaskのstaticディレクトリに保存
static_dir = os.path.join(os.getcwd(), 'static')
os.makedirs(static_dir, exist_ok=True)  # staticディレクトリがなければ作成


# OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
MAP=folium.Map(location=[41.76425725665729, 140.71906852658879], zoom_start=17)


# グラフを作成 OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
G = nw.Graph()


# 実際の座標 (仮のGPS座標に対応するリアルな座標) OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
real_pos = {
    1: (41.76787559000197, 140.71841883790933),2: (41.76701764202955, 140.7168410021742),3: (41.76680394095466, 140.7163782477871),4: (41.76625405052659, 140.71532342836053),5: (41.76765315465873, 140.71994591182036),
    6: (41.765679122994534, 140.71614734408772),7: (41.765396025625414, 140.71584097156602),8: (41.767940499638264, 140.7214607722791),9: (41.76722186565391, 140.72040123913928),10: (41.766910534438445, 140.71996111350379),
    11: (41.766665301177575, 140.71963457972345),12: (41.765610536931874, 140.71809209137928),13: (41.76531914717865, 140.7175232585814),14: (41.76512556287526, 140.71694023588154),15: (41.764873879346304, 140.71673850047537),
    16: (41.7643337552793, 140.7161632366974),17: (41.763672751345446, 140.71543671673504),18: (41.76763241844345, 140.72185773923175),19: (41.767122978430294, 140.7211729675175),20: (41.76689011009453, 140.72083018347118),
    21: (41.76655331055847, 140.7203478213156),22: (41.76630110463972, 140.719953150732),23: (41.76530173970925, 140.71826811125064),24: (41.76670448161581, 140.72168665015786),25: (41.766480954981006, 140.72136164253183),
    26: (41.766170213862296, 140.72077134768566),27: (41.765945370271616, 140.7203089430559),28: (41.76500260850722, 140.7184827187487),29: (41.76471045696296, 140.7178689469646),30: (41.76565047420439, 140.7206449935375),
    31: (41.764698683757885, 140.7187283208032),32: (41.76599541280083, 140.72201441951137),33: (41.765538687079186, 140.72145521996163),34: (41.765262745336976, 140.72108090915748),35: (41.764245967108224, 140.71909937395958),
    36: (41.763959428473825, 140.7173253067484),37: (41.763437053082924, 140.71705154779647),38: (41.76284619788241, 140.71671004197066),39: (41.76516079682868, 140.7218508245152),40: (41.764828009907454, 140.72156119325965),
    41: (41.76436008006294, 140.72066240376995),42: (41.76458161489887, 140.72184735470117),43: (41.76408969638268, 140.72089148411135),44: (41.76383596546081, 140.72030580552743),45: (41.763560531784954, 140.7195199540432),
    46: (41.76320615954464, 140.71868362553786),47: (41.76290808210021, 140.71800394371243),48: (41.7633654362151, 140.71965558430287),49: (41.76429463336831, 140.7221603810033),50: (41.76392437811024, 140.7216707342825),
    51: (41.76364482101068, 140.7212852877368),52: (41.76321212709298, 140.72068669582768),53: (41.76487348615491, 140.71526617453378),54: (41.7642160497022, 140.7145516868696),55: (41.76606774202388, 140.71485927825785),
    56: (41.76642929559674, 140.71462777895414),57: (41.76575747709037, 140.71384360401055),58: (41.765099536335036, 140.71313071756023),59: (41.76720483416704, 140.71344310564191),60: (41.766498678692706, 140.71264598222962),
    61: (41.76583980002719, 140.7119188333378),62: (41.76790961638468, 140.71212646226246),63: (41.76723603132305, 140.71144887729264),64: (41.766578940468776, 140.710723209774),65: (41.76877413630138, 140.71127273371684),
    66: (41.76852354653543, 140.71040322244988),67: (41.7683495024274, 140.70980844259228),68: (41.76813147923365, 140.70915429092005),69: (41.769326063486425, 140.71091056476567),
    
    100:(41.82355603658632, 140.72265516325547),101:(41.82361250230045, 140.72281140193),102:(41.78361635683899, 140.8024681340826),
    
    'A': (41.767471388768634, 140.71883395050202), # ラビスタ函館ベイ
    'B': (41.76479541845942, 140.72026412481048), # 豊川コモンズ
    'C': (41.765794833521355, 140.72175519612617), # メゾン・プレジデント
    'D': (41.76334346594526, 140.72148335441418), # 道営住宅高田屋通団地1号棟
    'E': (41.763951917840295, 140.72053725428955), # 市営豊川特定公共賃貸住宅
    'F': (41.76355775784047, 140.72046377669153), # 市営豊川改良団地
    'G': (41.764025922343365, 140.71823361067595), # アクロス十字街
    'H': (41.76313219954219, 140.71687006871647), # ヴィラコンコルディア
    'I': (41.76851235552426, 140.7087389068847) # 弥生小学校
}
# エッジと距離を追加 2(13,30)だけ車の距離 OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
edges_with_distances = [
    (1, 'A', 57),(1,2,160),(2,3,45),(2,12,180),(3,4,110),(3,13,190),(4,6,92),(5,9,57),(6,14,93),(6,7,40),(7,15,89),(8,18,49),(8,9,120),(9,20,51),(9,10,52),
    (10,21,52),(10,11,36),(11,'A',120),(11,22,53),(11,12,170),(12,23,33),(12,13,57),(13,29,75),(13,14,54),(14,15,35),(15,29,96),(15,16,78),(16,36,100),(16,17,94),(17,38,140),(18,19,81),(19,24,65),(19,20,38),
    (20,25,65),(20,21,56),(21,26,54),(21,22,44),(22,27,49),(22,23,180),(23,28,36),(24,25,37),(25,32,76),(25,26,61),(26,33,88),(26,27,45),(27,30,42),(27,28,180),(28,31,41),(28,29,62),
    (29,'G',80),(30,34,58),(30,31,190),(31,35,56),(32,'C',31),('C',33,39),(33,39,60),(33,34,46),(34,40,61),(34,'B',88),('B',41,59),('B',35,110),(35,45,85),(35,'G',72),('G',46,98),('G',36,76),(36,37,63),
    (37,47,99),(37,'H',37),('H',38,31),(39,40,45),(40,42,32),(40,41,92),(41,43,33),(42,49,39),(42,43,96),(43,51,58),(43,'E',33),('E',44,22),(44,'F',33),(44,45,71),(45,48,26),(45,46,79),
    (46,47,65),(48,'F',71),('F',52,44),(49,50,58),(50,51,45),(51,'D',38),(51,52,70),
    (7,53,75),(16,53,92),(17,54,93),(53,54,95),(7,55,110),(4,55,46),(55,56,49),(53,57,150),(54,58,150),(56,59,130),(56,57,99),(57,58,95),(57,60,130),(58,61,130),(59,62,140),(59,60,100),(60,63,130),(60,61,95),(61,64,130),(62,65,120),(62,63,110),(63,66,170),(63,64,93),(64,68,210),(65,69,68),(65,66,79),(66,67,54),(67,68,60),(68,'I',52),
    (18,100,7400),(101,100,5),(102,18,9)
]



def get_location():
    """
    現在位置を取得する関数。
    'location.json' ファイルから位置データを読み込む。
    """
    try:
        with open('location.json', 'r') as f:
            location_data = json.load(f)
        # 緯度と経度を返す
        return location_data['latitude'], location_data['longitude']
    except FileNotFoundError:
        print("Error: 'location.json' file not found.")
        return None
    except KeyError:
        print("Error: 'location.json' file does not contain the required keys.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode 'location.json'.")
        return None

def get_gps_coordinates():
    """
    get_locationで取得した座標を返す関数。
    取得に失敗した場合はNoneを返す。
    """
    location = get_location()  # get_locationで現在位置を取得
    if location is None:
        print("Failed to retrieve location.")
        return None
    return location


#def get_gps_coordinates():
    # テスト用の仮の座標
#    return (41.769326063486425, 140.71091056476567)


#辺をグラフGに追加しつつ、ノードも追加
for u, v, distance in edges_with_distances:
    G.add_edge(u, v, distance=distance)

    
# アルファベットのノードに特別な表示 (例えば、アイコンや画像)
alphabet_nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


# アルファベットのノードのポップアップに表示する画像
popup_images = {
    'A': "static/gazou/ラビスタ函館ベイ.png",
    'B': "static/gazou/豊川コモンズ.png",
    'C': "static/gazou/メゾン・プレジデント.png",
    'D': "static/gazou/道営住宅高田屋通団地1号棟.png",
    'E': "static/gazou/市営豊川特定公共賃貸住宅.png",
    'F': "static/gazou/市営豊川改良団地.png",
    'G': "static/gazou/アクロス十字街.png",
    'H': "static/gazou/ヴィラコンコルディア.png",
    'I': "static/gazou/弥生小学校.png"
}


# 実座標にマーカーを追加する 
# アルファベットと避難所名の対応辞書
shelter_names = {
    'A': 'ラビスタ函館ベイ',
    'B': '豊川コモンズ',
    'C': 'メゾン・プレジデント',
    'D': '道営住宅高田屋通団地1号棟',
    'E': '市営豊川特定公共賃貸住宅',
    'F': '市営豊川改良団地',
    'G': 'アクロス十字街',
    'H': 'ヴィラコンコルディア',
    'I': '弥生小学校'
    # それぞれのアルファベットに対応する避難所の名前を追加
}


#避難所や数字のノードを表示させるためのアイコンや情報を制御
for node, (lat, lon) in real_pos.items():
    if node in alphabet_nodes:
        # アルファベットに対応する避難所の名前を取得
        shelter_name = shelter_names.get(node, f'避難所 {node}')  # 辞書にない場合はデフォルトで避難所 {node}
        icon_url = "static/gazou/避難所.png"
        popup_image_url = popup_images.get(node)
        if icon_url and popup_image_url:
            icon = folium.CustomIcon(icon_url, icon_size=(30, 30), icon_anchor=(15, 15))
            
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(f"""<b>{shelter_name}</b><br>
                                        緯度: {lat}<br>
                                        経度: {lon}<br>
                                        <img src="{popup_image_url}" alt="{shelter_name}" width="150">""", max_width=200),
                icon=icon
            ).add_to(MAP)
    else:
        # 通常のノードには数字を付けたカスタムアイコンを使用
        folium.Marker(
            [lat, lon],
            popup=f"{node}番<br>緯度: {lat}<br>経度: {lon}",  # ポップアップに座標情報を表示
            icon=folium.DivIcon(
                html=f"""<div style="font-size: 11pt; color: blue; text-align: center;
                background-color: lightblue; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center;">
                {node}
            </div>""",
                # マーカーのサイズと位置を調整
                icon_size=(30, 30),
                icon_anchor=(15, 15)  # 中央に表示するためのアンカー
            )
        ).add_to(MAP)
        
    
    # --- エッジを黒線で描画する部分を追加 ---
# エッジを folium.PolyLine で描画
for u, v, distance in edges_with_distances:
    # u, v の実際の位置 (緯度・経度) を取得
    u_pos = real_pos[u]
    v_pos = real_pos[v]
    
    
    # 2点間に黒い線を引く (エッジを表現)
    folium.PolyLine(locations=[u_pos, v_pos], color='black', weight=2).add_to(MAP)


# 2点間の距離を計算する関数 (ユークリッド距離)
def calculate_distance(coord1, coord2):
    # 文字列が渡された場合、floatに変換
    coord1 = (float(coord1[0]), float(coord1[1]))
    coord2 = (float(coord2[0]), float(coord2[1]))
    
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)


# 実座標から最寄りのノードを見つける関数
def find_nearest_node_in_real_space(gps_coord, real_pos):
    nearest_node = None
    min_distance = float('inf')

    for node, node_real_pos in real_pos.items():
        distance = calculate_distance(gps_coord, node_real_pos)
        if distance < min_distance:
            min_distance = distance
            nearest_node = node

    return nearest_node


# 仮のGPSデータを取得
gps_coord = get_gps_coordinates()

if gps_coord:
    print(f"現在の位置は: 緯度 {gps_coord[0]}, 経度 {gps_coord[1]}")
else:
    print("位置情報の取得に失敗しました")
    

# GPS座標に最も近いノードを探す
nearest_node = find_nearest_node_in_real_space(gps_coord, real_pos)
print(f"現在地に最も近い地点は: {nearest_node}番です")


# 最短経路を計算
start_node = nearest_node
shortest_path = None
nearest_alpha_node = None
min_distance = float('inf')


for alpha_node in alphabet_nodes:
    try:
        # エッジの距離を考慮して最短経路を計算
        path_length = nw.shortest_path_length(G, source=start_node, target=alpha_node, weight='distance')
        if path_length < min_distance:
            min_distance = path_length
            shortest_path = nw.shortest_path(G, source=start_node, target=alpha_node, weight='distance')
            nearest_alpha_node = alpha_node
    except nw.NetworkXNoPath:
        continue  # 経路がない場合はスキップ


if shortest_path:
    print(f"最短経路: {shortest_path}")
    print(f"最寄りの避難所まで: {min_distance} m")
    estimated_time = min_distance / 80  # 80 m/minで移動すると仮定
    minutes = int(estimated_time)  # 分を取得
    seconds = (estimated_time - minutes) * 60  # 小数部分を秒に変換
    print(f"所要時間: {minutes}分 {seconds:.0f}秒")
    

# 避難所の名前を取得
shelter_name = shelter_names.get(nearest_alpha_node, "不明な避難所")
popup_image_url = popup_images.get(nearest_alpha_node)


nearest_alpha_node_real_pos = real_pos[nearest_alpha_node]
folium.Marker(
    nearest_alpha_node_real_pos,
    popup=folium.Popup(f"""<b>最寄りの避難所: {shelter_name}</b><br>
                           <img src="{popup_image_url}" alt="{shelter_name}" width="150"><br>
                           距離: {min_distance:.0f} m<br>
                           推定時間: {minutes}分 {seconds:.0f}秒""",
                       max_width=200),  # max_widthはここで指定
    icon=folium.CustomIcon("static/gazou/避難所.png", icon_size=(30, 30))
).add_to(MAP)


# 最短経路をハイライトして再描画
if shortest_path:
    for i, node in enumerate(shortest_path):
        if node not in alphabet_nodes:
            if i == 0:
                # スタート地点（最初のノード
                folium.Marker(
                    real_pos[node],
                    popup=f"{node}番<br>緯度: {real_pos[node][0]}<br>経度: {real_pos[node][1]}",
                    icon=folium.DivIcon(
                        html=f"""<div style="font-size: 11pt; color: white; text-align: center;
                        background-color: red; border-radius: 50%; border: 3px solid red; 
                        width: 25px; height: 25px; display: flex; align-items: center; justify-content: center;">
                        {node}
                    </div>""",
                        icon_size=(30, 30),
                        icon_anchor=(15, 15)
                    )
                ).add_to(MAP)
            else:
                # スタート地点以外は通常のオレンジ色のマーカー
                folium.Marker(
                    real_pos[node],
                    popup=f"{node}番<br>緯度: {real_pos[node][0]}<br>経度: {real_pos[node][1]}",
                    icon=folium.DivIcon(
                        html=f"""<div style="font-size: 11pt; color: white; text-align: center;
                        background-color: blue; border-radius: 50%; width: 25px; height: 25px;
                        display: flex; align-items: center; justify-content: center;">
                        {node}
                    </div>""",
                        icon_size=(30, 30),
                        icon_anchor=(15, 15)
                    )
                ).add_to(MAP)
                

    # 最短経路の線をオレンジ色に設定
    for u, v in zip(shortest_path, shortest_path[1:]):
        folium.PolyLine([real_pos[u], real_pos[v]], color="orange", weight=7).add_to(MAP)


# HTMLファイルをstaticディレクトリに保存
html_file_path = os.path.join(static_dir, 'map_with_path.html')

# 地図を保存
MAP.save(html_file_path)
print(f"地図を '{html_file_path}' に保存しました。")
