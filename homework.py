from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    PYTKA_POPYTKA: ClassVar[str] = (   # я не понимаю как тут надо исправить..можете накинуть материал или перефразировать комментарий?
        f'Тип тренировки: {self.training_type}; '
        f'Длительность: {self.duration:.{3}f} ч.; '
        f'Дистанция: {self.distance:.{3}f} км; '
        f'Ср. скорость: {self.speed:.{3}f} км/ч; '
        f'Потрачено ккал: {self.calories:.{3}f}'
    )

    def get_message(self) -> str:  # ??
        return self.PYTKA_POPYTKA(
            self.training_type, self.duration,
            self.distance, self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    MUR_MUR_1 = 18
    MUR_MUR_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.MUR_MUR_1 * self.get_mean_speed() - self.MUR_MUR_2)
                * self.weight / self.M_IN_KM * self.duration * self.H_IN_M)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        PUP_PUP_1 = 0.035
        PUP_PUP_2 = 0.029

        return (((PUP_PUP_1 * self.weight)
                + ((self.get_mean_speed() ** 2 // self.height)
                * PUP_PUP_2 * self.weight))
                * self.duration * self.H_IN_M)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        WOB_WOB_1 = 1.1
        WOB_WOB_2 = 2

        return (
            (self.get_mean_speed() + WOB_WOB_1)
            * WOB_WOB_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TYPE = {
        'WLK': SportsWalking,
        'RUN': Running,
        'SWM': Swimming
    }
    ERROR_404 = 'Упс, нет такой тренировки {}'

    if workout_type in TYPE:
        active_class = TYPE.get(workout_type)
        info_error(active_class, data)
        return TYPE.get(workout_type)(*data)
    raise ValueError(ERROR_404.format(workout_type))


def main(training: Training) -> None:
    """Главная функция."""
    print(Training.show_training_info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
