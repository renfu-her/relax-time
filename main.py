"""主程式入口"""
import sys
from controllers.timer_controller import TimerController


def main():
    """主函數"""
    # 檢查是否要在啟動時隱藏
    start_hidden = "--hidden" in sys.argv or "-h" in sys.argv
    
    # 創建控制器並運行
    controller = TimerController()
    
    try:
        controller.run(start_hidden=start_hidden)
    except KeyboardInterrupt:
        print("\n程式被用戶中斷")
    except Exception as e:
        print(f"發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.exit_app()


if __name__ == "__main__":
    main()

