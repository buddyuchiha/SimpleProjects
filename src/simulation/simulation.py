import threading
import time

from collections import deque
from random import choice

from base.base import Entity, Point
from entities.dynamic import Creature, Herbivore, Predator
from entities.static import Grass, Rock, Tree


class Simulation():
    def __init__(self, size: int):
        self.map = self.Map(size)
        self.renderer = self.Renderer(self.map)
        self.action = self.Action(self.map)
        self.counter = 0

        self.running = False
        self.input_thread = threading.Thread(target=self.choice_method())
        self.thread = None
        
        self.input_thread.start()
        
    def next_turn(self) -> None:
        if self.running:
            while self.running:
                print(f"Ход: {self.counter}")
                self.renderer.print_map()
                self.action.turn_actions() 
                
                time.sleep(1)
                self.counter += 1
                
        else:
            print(f"Ход: {self.counter}")
            self.renderer.print_map()
            self.action.turn_actions() 
            
            self.counter += 1

    
    def start_simulation(self):
        if not self.running:
            self.running = True 
            self.thread = threading.Thread(target=self.next_turn)
            self.thread.start()
    
    def pause_simulation(self):
        if self.running:
            print("Симуляция остановлена")
            self.running = False 
            self.thread.join()
        else:
            print("Симуляция уже и так приостановлена")
    
    def choice_method(self):
        print("\n" + "="*50)
        print(" "*13 + "ДОБРО ПОЖАЛОВАТЬ В СИМУЛЯЦИЮ")
        print("="*50)
        
        print("\nДоступные команды:\n")
    
        commands = [
            ("nextTurn()", "Просимулировать и отрендерить один ход"),
            ("startSimulation()", "Запустить бесконечный цикл симуляции"),
            ("pauseSimulation()", "Приостановить симуляцию"),
            ("exit", "Выйти из программы")
        ]
        
        for i, (cmd, desc) in enumerate(commands, 1):
            print(f"{i}. {cmd:<20} ┃ {desc}")
        
        print("\n" + "~"*50)
        print("Выберите действие (введите номер или название): ", end="")
        
        while True:
            choice = input().strip().lower()
            
            if choice in ("1", "nextturn", "nextturn()"):
                self.next_turn()
            elif choice in ("2", "startsimulation", "startsimulation()"):
                self.start_simulation()
            elif choice in ("3", "pausesimulation", "pausesimulation()"):
                self.pause_simulation()
            elif choice in ("4", "exit", "quit"):
                print("\nЗавершение работы симуляции...")
                self.running = False
                break
            else:
                print("Неверный ввод! Пожалуйста, попробуйте еще раз: ", end="")

    
    class Map():
        def __init__(self, size=None):
            self.size = size
            self.map_dict = {}
        
        def del_entity(self, point: Point) -> None: 
            self.map_dict.pop(point)
                
        def add_entity(self, point: Point, obj: Entity) -> None:
            map_obj = obj(point)
            self.map_dict[point] = map_obj 

        def move_entity(self, point: Point, obj: Creature, goal_point):
            self.del_entity(point)
            obj.point = goal_point
            self.map_dict[goal_point] = obj
         
        def get_object(self, obj: Herbivore | Predator) -> Grass | Herbivore:
            if isinstance(obj, Herbivore):
                obj = Grass
                
            elif isinstance(obj, Predator):
                obj = Herbivore
                
            return obj
         
        def get_entity_count(self, obj: Entity) -> int:
            objects = [
                value for value in self.map_dict.values() 
                if isinstance(value, obj)
                ]     
            return len(objects)
        
        def get_available_points(self) -> list[Point]:
            available = []
            for x in range(self.size):
                for y in range(self.size):
                    point = Point(x, y)
                    if point not in self.map_dict:
                        available.append(point)
            return available
         
        def is_reachable(self, point: Point, obj: Creature) -> bool:
            entity = self.map_dict.get(point)
            
            if isinstance(entity, Rock):
                return False
                
            if isinstance(obj, Herbivore):
                return entity is None or isinstance(entity, Grass)
            
            elif isinstance(obj, Predator):
                return entity is None or isinstance(entity, Herbivore)
            
            return False

        def bfs_shortest_path(
            self,
            start_point: Point,
            goal_point: Point,
            obj: Entity
            ) -> list[tuple[int, int]]:
            queue = deque([(start_point, [])])
            visited = set([start_point])
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                current_point, path = queue.popleft()

                if current_point == goal_point:
                    return path

                for dx, dy in directions:
                    neighbor = Point(
                        current_point.x + dx, 
                        current_point.y + dy
                        )

                    if not (0 <= neighbor.x < self.size \
                        and 0 <= neighbor.y < self.size):
                        continue

                    if neighbor not in visited:
                        entity = self.map_dict.get(neighbor)
                        
                        if entity is None or (neighbor == goal_point \
                            and self.is_reachable(neighbor, obj)):
                            visited.add(neighbor)
                            queue.append((neighbor, path + [(dx, dy)]))
                            
                        else:
                            visited.add(neighbor)  
            return []  
               
        def get_positions(
            self,
            obj: Entity
            ) -> list[Point]:
            positions = [
                point for point, entity in self.map_dict.items() 
                if isinstance(entity, obj)
            ]
            return positions
         
        def get_goal_point(
            self,
            point: Point,
            obj: Entity
            ) -> Point:
            obj = self.get_object(obj)    
            positions = self.get_positions(obj)
            
            if not positions: 
                return [] 
            
            manh_metr = []
            for goal_point in positions:
                manh_metr.append(
                    abs(point.x - goal_point.x) + abs(point.y - goal_point.y)
                    )
            return positions[manh_metr.index(min(manh_metr))]
        
        def move_predator(self, point: Point, obj: Predator) -> None:
            goal = self.get_goal_point(point, obj)
            if not goal:
                return
            
            target = self.map_dict.get(goal)
            if not target or not isinstance(target, Herbivore):
                return
            
            path = self.bfs_shortest_path(point, goal, obj)
            
            if len(path) <= 1:
                if obj.try_attack(target):
                    self.del_entity(goal)
                    if goal not in self.map_dict:
                        self.move_entity(point, obj, goal)
            else:
                new_coord = obj.make_move(point, path)
                if new_coord not in self.map_dict:
                    self.move_entity(point, obj, new_coord)
                
        def move_herbivore(self, point: Point, obj: Herbivore) -> None:
            goal = self.get_goal_point(point, obj) 
            path = self.bfs_shortest_path(point, goal, obj)
            new_coord = obj.make_move(point, path)
            
            self.move_entity(point, obj, new_coord)
        
        def move_creature(self, point: Point, obj: Creature) -> None:
            if isinstance(obj, Predator):
                self.move_predator(point, obj)
                
            elif isinstance(obj, Herbivore):
                self.move_herbivore(point, obj)


    class Action():
        def __init__(self, map):
            self.map = map 
            
            dynamic_capacity = int(self.map.size * 0.5)
            static_capacity = int(self.map.size * 0.2)
            
            self.capacity = {
                Rock      : int(dynamic_capacity * 0.2),
                Tree      : int(dynamic_capacity * 0.3),
                Grass     : int(dynamic_capacity * 0.5),
                Herbivore : int(static_capacity * 0.5),
                Predator  : int(static_capacity * 0.5)
            }
                  
            self.reset_entities = [
                Grass, Herbivore    
            ]
            
            self.init_actions()
        
        def __random_cord(self) -> int:
            if not self.coords:
                raise ValueError(self.coords)
            
            coord = choice(self.coords)
            self.coords.remove(coord)
            
            return coord    
        
        def init_actions(self) -> None:
            for x in range(self.map.size):
                self.coords = [i for i in range(self.map.size)]
                
                for key, value in self.capacity.items():
                    for _ in range(value):
                        coord_y = self.__random_cord()
                        point = Point(x, coord_y)
                        self.map.add_entity(point, key)
                        
        def turn_actions(self) -> None:
            temp_map = self.map.map_dict.copy()
            for key, value in temp_map.items():
                if(isinstance(value, Creature)):
                    self.map.move_creature(key, value)
            
            for reset_entity in self.reset_entities:
                entity_count = self.map.get_entity_count(reset_entity) 
                
                points = self.map.get_available_points()                    
                if not points:  
                    continue
                
                entity_capacity = self.capacity.get(reset_entity) \
                    * int(self.map.size / 2)
                while entity_count < entity_capacity and points: 
                    point = choice(points)
                    self.map.add_entity(point, reset_entity)
                    
                    entity_count += 1
                    points.remove(point)
                                        
    
    class Renderer():
        def __init__(self, map):
            self.map = map 
            
        def print_map(self) -> None:
            for x in range(self.map.size):
                for y in range(self.map.size):
                    coord = Point(x, y)
                    print(self.map.map_dict.get(coord, '⬜️'), end='')
                print("\n")
            print("\n")
            