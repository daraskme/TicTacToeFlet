import flet as ft
import random

def main(page: ft.Page):
    page.title = "三目並べ AI対戦"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    current_player = "X"
    board = [""] * 9
    game_over = False
    ai_enabled = False

    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    status_text = ft.Text(
        f"次のプレイヤー: {current_player}",
        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        text_align=ft.TextAlign.CENTER,
        width=page.width
    )

    def check_winner():
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
                return board[combo[0]]
        if "" not in board:
            return "引き分け"
        return None

    def ai_move():
        empty_cells = [i for i, cell in enumerate(board) if cell == ""]
        if empty_cells:
            return random.choice(empty_cells)
        return None

    def update_button(index, player):
        board[index] = player
        buttons[index].content.value = player
        buttons[index].disabled = True
        if player == "X":
            buttons[index].content.color = ft.colors.WHITE
            buttons[index].bgcolor = ft.colors.BLACK
        else:
            buttons[index].content.color = ft.colors.BLACK
            buttons[index].bgcolor = ft.colors.WHITE
        buttons[index].content.size = 40
        buttons[index].content.weight = ft.FontWeight.BOLD

    def button_clicked(e):
        nonlocal current_player, game_over
        if game_over:
            return

        index = int(e.control.data)
        if board[index] == "":
            update_button(index, current_player)
            check_game_state()

            if not game_over and ai_enabled:
                ai_index = ai_move()
                if ai_index is not None:
                    current_player = "O"
                    update_button(ai_index, current_player)
                    check_game_state()

    def check_game_state():
        nonlocal current_player, game_over
        winner = check_winner()
        if winner:
            game_over = True
            if winner == "引き分け":
                status_text.value = "引き分けです！"
            else:
                status_text.value = f"プレイヤー {winner} の勝利！"
        else:
            current_player = "O" if current_player == "X" else "X"
            status_text.value = f"次のプレイヤー: {current_player}"
        page.update()

    def reset_game(e):
        nonlocal current_player, board, game_over
        current_player = "X"
        board = [""] * 9
        game_over = False
        status_text.value = f"次のプレイヤー: {current_player}"
        for button in buttons:
            button.content.value = ""
            button.disabled = False
            button.bgcolor = ft.colors.SURFACE_VARIANT
        page.update()

    def toggle_ai(e):
        nonlocal ai_enabled
        ai_enabled = ai_switch.value
        reset_game(None)

    buttons = [
        ft.ElevatedButton(
            content=ft.Text("", size=40, weight=ft.FontWeight.BOLD),
            width=100,
            height=100,
            data=str(i),
            on_click=button_clicked,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),
            )
        ) for i in range(9)
    ]

    board_ui = ft.Row(
        controls=[
            ft.Column(controls=buttons[i:i+3])
            for i in range(0, 9, 3)
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    reset_button = ft.ElevatedButton("リセット", on_click=reset_game)
    ai_switch = ft.Switch(label="AI対戦", on_change=toggle_ai)

    controls_row = ft.Row([reset_button, ai_switch], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column([
            status_text,
            board_ui,
            controls_row
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)