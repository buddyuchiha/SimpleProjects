import threading
import time

class Simulation():
    def __init__(self, 
                 map,
                 renderer,
                 action,
                 ) -> None:
        self.map = map
        self.renderer = renderer
        self.action = action
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

    def start_simulation(self) -> None:
        if not self.running:
            self.running = True 
            self.thread = threading.Thread(target=self.next_turn)
            self.thread.start()
    
    def pause_simulation(self) -> None:
        if self.running:
            print("Симуляция остановлена")
            self.running = False 
            self.thread.join()
        else:
            print("Симуляция уже и так приостановлена")
    
    @staticmethod
    def print_speech() -> None:
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
    
    def choice_method(self) -> None:
        self.print_speech()
        
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