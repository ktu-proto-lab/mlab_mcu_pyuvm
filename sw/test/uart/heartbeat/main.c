#include <stdint.h>

/**
 * @brief Base memory address of the GPIO peripheral.
 */
#define GPIO_BASE_ADDR 0x40000000

/**
 * @brief Bit definitions
 */
/* ----- Control register                                          */

#define ENABLE_INT (1 << 0)  /* Interrupt enable bit:              */
                             /*      1 - Interrupt enabled         */
                             /*      0 - Interrupt disabled        */
#define GLOBAL_INTS (1 << 1) /* Interrupt status bit               */
                             /*      1 - Interrupt is pending      */
                             /*      0 - No interrupt pending      */
                             /* Other bits in CR are reserved      */

/**
 * @brief  GPIO Bit SET and Bit RESET enumeration
 */
typedef enum { GPIO_PIN_RESET = 0, GPIO_PIN_SET } GPIO_PinState;

/**
 * @brief GPIO Peripheral register map
 */
typedef struct {
  volatile uint32_t IN;     // Input data
  volatile uint32_t OUT;    // Output data
  volatile uint32_t OE;     // Output enable
  volatile uint32_t INTE;   // Interrupt enable
  volatile uint32_t PTRIG;  // Interrupt trigger edge ( 0 - negedge, 1 - posedge)
  volatile uint32_t AUX;    // Multiplex auxiliary inputs to GPIO ( 0 - driven by
                            // OUT, 1- driven by aux
  volatile uint32_t CTRL;   // Control register
  volatile uint32_t INTS;   // Interrupt status
} GPIO_reg_map_t;
/**
 * @brief GPIO Handle
 */
typedef struct {
  volatile GPIO_reg_map_t *regs;
  uint32_t Interrupt_Status;
} GPIO_HandleTypeDef;

/**
 * @brief  GPIO Bit SET and Bit RESET enumeration
 */
#define GPIO_PIN_0 ((uint32_t)0x0001)  /* Pin 0 selected    */
#define GPIO_PIN_1 ((uint32_t)0x0002)  /* Pin 1 selected    */
#define GPIO_PIN_2 ((uint32_t)0x0004)  /* Pin 2 selected    */
#define GPIO_PIN_3 ((uint32_t)0x0008)  /* Pin 3 selected    */
#define GPIO_PIN_4 ((uint32_t)0x0010)  /* Pin 4 selected    */
#define GPIO_PIN_5 ((uint32_t)0x0020)  /* Pin 5 selected    */
#define GPIO_PIN_6 ((uint32_t)0x0040)  /* Pin 6 selected    */
#define GPIO_PIN_7 ((uint32_t)0x0080)  /* Pin 7 selected    */
#define GPIO_PIN_8 ((uint32_t)0x0100)  /* Pin 8 selected    */
#define GPIO_PIN_9 ((uint32_t)0x0200)  /* Pin 9 selected    */
#define GPIO_PIN_10 ((uint32_t)0x0400) /* Pin 10 selected    */
#define GPIO_PIN_11 ((uint32_t)0x0800) /* Pin 11 selected    */

void GPIO_Init(GPIO_HandleTypeDef *gpio);
void GPIO_WritePin(GPIO_HandleTypeDef *gpio, uint32_t GPIO_Pin, GPIO_PinState PinState);
void GPIO_Toggle(GPIO_HandleTypeDef *gpio, uint32_t GPIO_Pin);
void gpio_irq_handler(GPIO_HandleTypeDef *gpio);
void GPIO_EXTI_Callback(GPIO_HandleTypeDef *gpio) __attribute__((weak));


#ifndef UART_H
#define UART_h

#include <stdint.h>

/**
 * @brief Base memory address of the UART peripheral.
 */

#define UART_BASE_ADDR 0x50000000

#define UART_SETUP_BAUD_MASK 0xFFFFFF
#define UART_BAUD_INTERVAL(CPU_Freq, UART_Baudrate) (CPU_Freq * 1000000) / (UART_Baudrate);

/* ----- Bits definition                                                  */

/* ----- Setup register                                                   */

#define UART_N (1 << 28)    /*Indicates the number of data bits per word.
                              This will either be 2'b00 for an 8-bit word,
                              2'b01 for a 7-bit word, 2'b10 for a six bit
                              word, or 2'b11 for a five bit word.         */
#define UART_S (1 << 27)
#define UART_P (1 << 26)
#define UART_F (1 << 25)
#define UART_T (1 << 24)
#define UART_BAUD (1 << 0)


/* ----- Control register                                             */

#define UART_TX_RST (1 << 5)
#define UART_TX_INT_EN (1 << 4)
#define UART_TX_EN (1 << 3)
#define UART_RX_RST (1 << 2)
#define UART_RX_INT_EN (1 << 1)
#define UART_RX_EN (1 << 0)

/* ----- Receive register                                             */

#define UART_RX_C (1 << 13)
#define UART_RX_BREAK (1 << 12)
#define UART_RX_ERR (1 << 11)
#define UART_RX_FRAME_ERR (1 << 10)
#define UART_RX_PARITY_ERR (1 << 9)
#define UART_RX_EMPTY (1 << 8)
#define UART_RX_BYTE_WIDTH 8
#define UART_RX_BYTE (1 << 0)

/* ----- Transmit register                                            */

#define UART_TX_O (1 << 11)
#define UART_TX_BREAK (1 << 10)
#define UART_TX_BUSY (1 << 9)
#define UART_TX_EMPTY (1 << 8)
#define UART_TX_BYTE_WIDTH 8
#define UART_TX_BYTE (1 << 0)


/**
 * @brief UART peripheral register map.
 */

typedef struct {
  volatile uint32_t SETUP;   /* UART configuration / setup register     */
  volatile uint32_t CONTROL;  /* UART control, TX RX and int enable      */
  volatile uint32_t RX_DATA; /* Contains RX data                        */
  volatile uint32_t TX_DATA; /* Contains TX data                        */
} UART_reg_map_t;


/**
 * @brief UART peripheral configuration.
 */

typedef struct {
  uint32_t BaudRate;
  uint32_t WordLength;
  uint32_t StopBits;
  uint32_t Parity;
  uint32_t ParityMode;
  uint32_t ParityLock;
} UART_InitTypeDef;

typedef enum
{
  UART_STATE_RESET             = 0x00U,    /*!< Peripheral is not yet Initialized
                                                   Value is allowed for gState and RxState */

  UART_STATE_READY             = 0x20U,    /*!< Peripheral Initialized and ready for use
                                                   Value is allowed for gState and RxState */

  UART_STATE_BUSY              = 0x24U,    /*!< an internal process is ongoing
                                                   Value is allowed for gState only */

  UART_STATE_BUSY_TX           = 0x21U,    /*!< Data Transmission process is ongoing
                                                   Value is allowed for gState only */

  UART_STATE_BUSY_RX           = 0x22U,    /*!< Data Reception process is ongoing
                                                   Value is allowed for RxState only */

  UART_STATE_BUSY_TX_RX        = 0x23U,    /*!< Data Transmission and Reception process is ongoing
                                                   Not to be used for neither gState nor RxState.
                                                   Value is result of combination (Or) between gState and RxState values */

  UART_STATE_TIMEOUT           = 0xA0U,    /*!< Timeout state
                                                   Value is allowed for gState only */

  UART_STATE_ERROR             = 0xE0U     /*!< Error
                                                   Value is allowed for gState only */
} UART_StateTypeDef;

/**
 * @brief UART peripheral handle
 */

typedef struct {

    volatile UART_reg_map_t *Instance;      /*!< UART registers base address     */ 

    UART_InitTypeDef Init;                  /*!< UART communication parameters   */

    uint8_t *pTxBuffPtr;                 /*!< Pointer to UART Tx transfer Buffer */

    uint16_t TxXferSize;                    /*!< UART Tx Transfer size           */

    volatile uint16_t TxXferCount;          /*!< UART Tx Transfer Counter        */

    uint8_t *pRxBuffPtr;                 /*!< Pointer to UART Rx transfer Buffer */

    uint16_t RxXferSize;                    /*!< UART Rx Transfer size           */

    volatile uint16_t RxXferCount;          /*!< UART Rx Transfer Counter        */

    volatile UART_StateTypeDef gState;      /*!< UART state information related to
                                                 global Handle management and also
                                                 related to Tx operations. This
                                                 parameter can be a value of
                                                 @ref HAL_UART_StateTypeDef      */

    volatile UART_StateTypeDef RxState;     /*!< UART state information related to
                                                 Rx operations. This parameter can
                                                 be a value of @ref
                                                 HAL_UART_StateTypeDef           */
} UART_HandleTypeDef;

/**
 * @brief Initialize UART peripheral with specified settings defined in huart.Init struct
 */

void UART_Init(UART_HandleTypeDef *huart);

/**
 * @brief Enables UART TX port
 */

void UART_TX_Enable(UART_HandleTypeDef *huart);

/**
 * @brief Disables UART TX port
 */

void UART_TX_Disable(UART_HandleTypeDef *huart);

/**
 * @brief resets UART TX module
 */

void UART_TX_Reset(UART_HandleTypeDef *huart);

/**
 * @brief Enables UART RX port
 */

void UART_RX_Enable(UART_HandleTypeDef *huart);

/**
 * @brief Disables UART RX port
 */

void UART_RX_Disable(UART_HandleTypeDef *huart);

/**
 * @brief resets UART RX module
 */

void UART_RX_Reset(UART_HandleTypeDef *huart);

/**
 * @brief Blocking UART transmit
 */

void UART_Transmit(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size);

/**
 * @brief Blocking UART receive
 */

void UART_Receive(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size);

/**
 * @brief Non-Blocking UART transmit
 */

void UART_Transmit_IT(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size);

/**
 * @brief Non-Blocking UART receive
 */

void UART_Receive_IT(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size);

/**
 * @brief RX FIFO half-full interrupt handler
 */

void UART_RX_Not_Empty_IRQHandler(UART_HandleTypeDef *huart);

/**
 * @brief TX FIFO not-full interrupt handler
 */

void UART_TX_Not_Full_IRQHandler(UART_HandleTypeDef *huart);

/**
 * @brief UART_Receive_IT complete callback
 */

void UART_RxCpltCallback(UART_HandleTypeDef *huart);

/**
 * @brief UART_Transmit_IT complete callback
 */

void UART_TxCpltCallback(UART_HandleTypeDef *huart);

#endif


/**
 * @file gpio.c
 * @author Dovydas Liutkus (dovydas.liutkus@ktu.edu)
 * @version 0.1
 * @date 2025-08-11
 */

void GPIO_Init(GPIO_HandleTypeDef *gpio) {
  // Initialize register pointer to GPIO peripheral
  gpio->regs = (volatile GPIO_reg_map_t *)GPIO_BASE_ADDR;
}

/**
 * @brief  Sets or clears the selected data port bit.
 *
 * @param  GPIO_Pin specifies the port bit to be written.
 *         This parameter can be any combination of GPIO_PIN_x where x can be (0..11).
 * @param  PinState specifies the value to be written to the selected bit.GPIO_PinState
 *          This parameter can be one of the GPIO_PinState enum values:
 *            @arg GPIO_PIN_RESET: to clear the port pin
 *            @arg GPIO_PIN_SET: to set the port pin
 * @retval None
 */
void GPIO_WritePin(GPIO_HandleTypeDef *gpio, uint32_t GPIO_Pin, GPIO_PinState PinState) {
  if (PinState != GPIO_PIN_RESET) {
    gpio->regs->OUT |= GPIO_Pin;
  } else {
    gpio->regs->OUT &= ~GPIO_Pin;
  }
}
/**
 * @brief  Toggles the specified GPIO pins.
 * @param  GPIO_Pin Specifies the pins to be toggled.
 *         This parameter can be any combination of GPIO_PIN_x where x can be (0..11).
 * @retval None
 */
void GPIO_Toggle(GPIO_HandleTypeDef *gpio, uint32_t GPIO_Pin) {
  // XOR to toggle
  gpio->regs->OUT ^= GPIO_Pin;
}

void gpio_irq_handler(GPIO_HandleTypeDef *gpio) {
  // Record interrupt in handle and clear INTS register
  gpio->Interrupt_Status = gpio->regs->INTS;
  gpio->regs->INTS = 0;
  // Callback for User
  GPIO_EXTI_Callback(gpio);
}

#define NULL                ((void *) 0)

/* Everywhere you see return HAL_* - a lot needs to change for those returns
 * to mean anything. HAL_STATUS needs to be defined and some error handling
 * implemented.                                                             */


void UART_Init(UART_HandleTypeDef *huart)
{
/*
  if (huart == NULL)
  {
      return HAL_ERROR;
  }
*/
  if (huart->gState == UART_STATE_RESET)
  {
      huart->Instance = (volatile UART_reg_map_t *)UART_BASE_ADDR;  // Initialize UART registers struct

      // SETUP register shouldn't be edited anywhere else except in this function
      // After editing huart->Init UART_Init(*huart) should always be called
      huart->Instance->SETUP = ((huart->Init.BaudRate << 0) & UART_SETUP_BAUD_MASK)
          | (huart->Init.ParityMode << 24)
          | (huart->Init.ParityLock << 25)
          | (huart->Init.Parity << 26)
          | (huart->Init.StopBits << 27)
          | (huart->Init.WordLength << 28);

      huart->gState = UART_STATE_READY; // if TxEnable false dont set ready?
      huart->RxState = UART_STATE_READY;
  }
  else
  {
      // return HAL_ERROR
  }
}

void UART_TX_Enable(UART_HandleTypeDef *huart)
{
    if (huart->gState == UART_STATE_READY)
    {
        huart->Instance->CONTROL |= UART_TX_EN;
    }
}

void UART_TX_Disable(UART_HandleTypeDef *huart)
{
    if (huart->gState == UART_STATE_READY)
    {
        huart->Instance->CONTROL &= ~UART_TX_EN;
    }
}

void UART_TX_Reset(UART_HandleTypeDef *huart)
{
    /* State probably doesn't matter and it should be able to
     * execute whenever it's called                             */
    huart->Instance->CONTROL |= UART_TX_RST;
}

void UART_RX_Enable(UART_HandleTypeDef *huart)
{
    if (huart->RxState == UART_STATE_READY)
    {
        huart->Instance->CONTROL |= UART_RX_EN;
    }
}

void UART_RX_Disable(UART_HandleTypeDef *huart)
{
    if (huart->RxState == UART_STATE_READY)
    {
        huart->Instance->CONTROL &= ~UART_RX_EN;
    }
}

void UART_RX_Reset(UART_HandleTypeDef *huart)
{
    /* State probably doesn't matter and it should be able to
     * execute whenever it's called                             */
    huart->Instance->CONTROL |= UART_RX_RST;
}

void UART_Transmit(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size)
{
    // Check whether UART core is busy (for example interupt driven transmision is
    // in progress)
    if (huart->gState != UART_STATE_READY) {
        return;
    }
    if ((pData == NULL) || (Size == 0U))
    {
        // return HAL_ERROR;
        return;
    }
    while (Size > 0)
    {
        if (!(huart->Instance->TX_DATA & UART_TX_BUSY))
        {
            huart->Instance->TX_DATA = *pData;
            pData++;
            Size--;
        }
    }
    while (huart->Instance->TX_DATA & UART_TX_BUSY); // Wait unitl transmit ends
}

void UART_Transmit_IT(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size)
{
    /* Check that a Tx process is not already ongoing */
    if (huart->gState != UART_STATE_READY)
    {
        // return HAL_BUSY;
        return;
    }
    if ((pData == NULL) || (Size == 0U))
    {
        // return HAL_ERROR;
        return;
    }

    huart->pTxBuffPtr = pData;
    huart->TxXferSize = Size;
    huart->TxXferCount = Size;

    huart->gState = UART_STATE_BUSY_TX;

    // Enable interrupt
    huart->Instance->CONTROL |= UART_TX_INT_EN;

    // return HAL_OK;
}



void UART_Receive(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size)
{
    while (Size > 0)
    {
        uint16_t rx_data = huart->Instance->RX_DATA;
        // Interrupt automaticaly acknowledges after second read from RX_DATA register
        if (rx_data & UART_RX_EMPTY)
        {
            *pData++ = rx_data;
            Size--;
        }
    }
}

void UART_Receive_IT(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size)
{
    /* Check that a Rx process is not already ongoing */
    if (huart->RxState == UART_STATE_READY)
    {
        if ((pData == NULL) || (Size == 0U))
        {
            // return HAL_ERROR;
        }

        huart->pRxBuffPtr = pData;
        huart->RxXferSize = Size;
        huart->RxXferCount = Size;

        huart->RxState = UART_STATE_BUSY_RX;

        // Enable interrupt
        huart->Instance->CONTROL |= (1 << 1);

        // return HAL_OK;
    }
    else
    {
        // return HAL_BUSY;
    }
}

void UART_RX_Not_Empty_IRQHandler(UART_HandleTypeDef *huart)
{
    if(huart->RxState == UART_STATE_BUSY_RX)
    {   
        *(huart->pRxBuffPtr) = huart->Instance->RX_DATA;
        
        if(huart->RxXferCount == 1)
        {
            // disable interrupt
            huart->Instance->CONTROL &= ~UART_RX_INT_EN;

            // enable CpltCallback
            UART_RxCpltCallback(huart);

            huart->RxState = UART_STATE_READY;
        }
        huart->pRxBuffPtr++;
        huart->RxXferCount--;
        
        
        // return HAL_OK;
    }
    else
    {
        // return HAL_BUSY;
    }
}

void UART_TX_Not_Full_IRQHandler(UART_HandleTypeDef *huart)
{
    if(huart->gState == UART_STATE_BUSY_TX)
    {
        
        if(huart->TxXferCount == 0)
        {
            /* disable interrupt                                            */
            huart->Instance->CONTROL &= ~UART_TX_INT_EN;


            huart->gState = UART_STATE_READY; /* There's probably a better way
                                                 to handle this, refer to
                                                 STM32_HAL                  */
            
            /* enable CpltCallback                                          */
            UART_TxCpltCallback(huart);
                                    
        }
        else{
            huart->Instance->TX_DATA = *(huart->pTxBuffPtr);
        }
        
        huart->pTxBuffPtr++;
        huart->TxXferCount--;

        // return HAL_OK;
    }
    else
    {
        // return HAL_BUSY;
    }
}

#define CPUFreq 80     // MHz
#define UART_BAUDRATE 115200

GPIO_HandleTypeDef gpio;
UART_HandleTypeDef huart;

void __attribute__((interrupt)) GPIO_IRQHandler(void) { while(1); }

void __attribute__((interrupt)) I2C_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) TIMER_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_HALF_FULL_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_HALF_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_NOT_EMPTY_IRQHandler(void) { 
    UART_RX_Not_Empty_IRQHandler(&huart);
}

void __attribute__((interrupt)) UART_TX_NOT_FULL_IRQHandler(void) ;

void UART_TX_NOT_FULL_IRQHandler(void) { 
    UART_TX_Not_Full_IRQHandler(&huart);
}

void DEFAULT_IRQHandler(void) { while (1); }


int main() {
    GPIO_Init(&gpio);
    huart.Init.BaudRate = UART_BAUD_INTERVAL(CPUFreq, UART_BAUDRATE);
    huart.Init.WordLength = 0;
    huart.Init.StopBits = 0;
    huart.Init.Parity = 0;
    huart.Init.ParityMode = 0;
    huart.Init.ParityLock = 0;
    UART_Init(&huart);
    UART_TX_Enable(&huart);
    gpio.regs->AUX |= GPIO_PIN_1;
    gpio.regs->OE  |= GPIO_PIN_1;
    uint8_t buffer[] = "hello uart";
    UART_Transmit(&huart, buffer, sizeof(buffer));
    while(1);
}

void UART_TxCpltCallback(UART_HandleTypeDef *huart) {}
void UART_RxCpltCallback(UART_HandleTypeDef *huart) {}
