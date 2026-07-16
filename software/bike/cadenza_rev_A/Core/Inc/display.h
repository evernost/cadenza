

#ifndef INC_DISPLAY_H_
#define INC_DISPLAY_H_


#define REG_EFLAG0          0x46
#define REG_EFLAG1          0x47
#define REG_EFLAG2          0x48
#define REG_EFLAG3          0x49

#define AUTO_INC_OPT        (1 << 7)


typedef struct __SPI_HandleTypeDef
{
  SPI_TypeDef                *Instance;      /*!< SPI registers base address               */
  SPI_InitTypeDef            Init;           /*!< SPI communication parameters             */
  const uint8_t              *pTxBuffPtr;    /*!< Pointer to SPI Tx transfer Buffer        */
  uint16_t                   TxXferSize;     /*!< SPI Tx Transfer size                     */
  __IO uint16_t              TxXferCount;    /*!< SPI Tx Transfer Counter                  */
  uint8_t                    *pRxBuffPtr;    /*!< Pointer to SPI Rx transfer Buffer        */
  uint16_t                   RxXferSize;     /*!< SPI Rx Transfer size                     */
  __IO uint16_t              RxXferCount;    /*!< SPI Rx Transfer Counter                  */
  void (*RxISR)(struct __SPI_HandleTypeDef *hspi);   /*!< function pointer on Rx ISR       */
  void (*TxISR)(struct __SPI_HandleTypeDef *hspi);   /*!< function pointer on Tx ISR       */
  DMA_HandleTypeDef          *hdmatx;        /*!< SPI Tx DMA Handle parameters             */
  DMA_HandleTypeDef          *hdmarx;        /*!< SPI Rx DMA Handle parameters             */
  HAL_LockTypeDef            Lock;           /*!< Locking object                           */
  __IO HAL_SPI_StateTypeDef  State;          /*!< SPI communication state                  */
  __IO uint32_t              ErrorCode;      /*!< SPI Error code                           */
} SPI_HandleTypeDef;



typedef struct __Display_HandleTypeDef
{
  uint8_t[6] digits;
  uint8_t accel;
} Display_HandleTypeDef;




// Public
void ledInitDriver(void);
void ledUpdateFace(rgbLedType (*)[9], uint8_t);
void ledUpdate(rgbLedType (*)[9]);


#endif /* INC_DISPLAY_H_ */
