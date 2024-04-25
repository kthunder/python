#ifdef __cplusplus
extern "C"
{
#endif

// .c
static void (*FuncPtr)() = &a;
FuncPtrType FuncPtr;

// .h
typedef void (*FuncPtrType)();
extern FuncPtrType FuncPtr;


#include "Demo.h"
#include "Demo_Cfg.h"
#include <stdio.h>

#define TEST_ARR(arr) printf("addr: 0x%08X val: %08X name: %s\r\n", (uint32)(void *)arr, (uint32)arr[0], #arr);
#define TEST_STRUCT(st, member) printf("addr: 0x%08X val: %08X name: %s.%s \r\n", (uint32)(void *)&st, st.member, #st, #member);

#define DEMO_START_SEC_VAR_INIT_BOOLEAN
#include "Demo_MemMap.h"
    boolean DemoVarInitBool[] = {TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE};
#define DEMO_STOP_SEC_VAR_INIT_BOOLEAN
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_INIT_8
#include "Demo_MemMap.h"
    uint8 DemoVarInit8[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_VAR_INIT_8
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_INIT_16
#include "Demo_MemMap.h"
    uint16 DemoVarInit16[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_VAR_INIT_16
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_INIT_32
#include "Demo_MemMap.h"
    uint32 DemoVarInit32[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_VAR_INIT_32
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_INIT_PTR
#include "Demo_MemMap.h"
    uint8 *DemoVarInitPtr[] = {(uint8 *)0x1000};
#define DEMO_STOP_SEC_VAR_INIT_PTR
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_INIT_UNSPECIFIED
#include "Demo_MemMap.h"
    DemoUnspecifiedTpye DemoVarInitUnspecified = {1, 2, 3};
#define DEMO_STOP_SEC_VAR_INIT_UNSPECIFIED
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_INIT_BOOLEAN
#include "Demo_MemMap.h"
    boolean DemoVarFastInitBool[] = {TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE};
#define DEMO_STOP_SEC_VAR_FAST_INIT_BOOLEAN
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_INIT_8
#include "Demo_MemMap.h"
    uint8 DemoVarFastInit8[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_VAR_FAST_INIT_8
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_INIT_16
#include "Demo_MemMap.h"
    uint16 DemoVarFastInit16[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_VAR_FAST_INIT_16
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_INIT_32
#include "Demo_MemMap.h"
    uint32 DemoVarFastInit32[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_VAR_FAST_INIT_32
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_INIT_PTR
#include "Demo_MemMap.h"
    uint8 *DemoVarFastInitPtr[] = {(uint8 *)0x1000};
#define DEMO_STOP_SEC_VAR_FAST_INIT_PTR
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_INIT_UNSPECIFIED
#include "Demo_MemMap.h"
    DemoUnspecifiedTpye DemoVarFastInitUnspecified = {1, 2, 3};
#define DEMO_STOP_SEC_VAR_FAST_INIT_UNSPECIFIED
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_CLEARED_BOOLEAN
#include "Demo_MemMap.h"
    boolean DemoVarClearedBool[] = {FALSE};
#define DEMO_STOP_SEC_VAR_CLEARED_BOOLEAN
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_CLEARED_8
#include "Demo_MemMap.h"
    uint8 DemoVarCleared8[] = {0};
#define DEMO_STOP_SEC_VAR_CLEARED_8
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_CLEARED_16
#include "Demo_MemMap.h"
    uint16 DemoVarCleared16[] = {0};
#define DEMO_STOP_SEC_VAR_CLEARED_16
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_CLEARED_32
#include "Demo_MemMap.h"
    uint32 DemoVarCleared32[] = {0};
#define DEMO_STOP_SEC_VAR_CLEARED_32
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_CLEARED_PTR
#include "Demo_MemMap.h"
    uint8 *DemoVarClearedPtr[] = {0};
#define DEMO_STOP_SEC_VAR_CLEARED_PTR
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_CLEARED_UNSPECIFIED
#include "Demo_MemMap.h"
    DemoUnspecifiedTpye DemoVarClearedUnspecified = {0, 0, 0};
#define DEMO_STOP_SEC_VAR_CLEARED_UNSPECIFIED
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_CLEARED_BOOLEAN
#include "Demo_MemMap.h"
    boolean DemoVarFastClearedBool[] = {FALSE};
#define DEMO_STOP_SEC_VAR_FAST_CLEARED_BOOLEAN
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_CLEARED_8
#include "Demo_MemMap.h"
    uint8 DemoVarFastCleared8[] = {0};
#define DEMO_STOP_SEC_VAR_FAST_CLEARED_8
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_CLEARED_16
#include "Demo_MemMap.h"
    uint16 DemoVarFastCleared16[] = {0};
#define DEMO_STOP_SEC_VAR_FAST_CLEARED_16
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_CLEARED_32
#include "Demo_MemMap.h"
    uint32 DemoVarFastCleared32[] = {0};
#define DEMO_STOP_SEC_VAR_FAST_CLEARED_32
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_CLEARED_PTR
#include "Demo_MemMap.h"
    uint8 *DemoVarFastClearedPtr[] = {0};
#define DEMO_STOP_SEC_VAR_FAST_CLEARED_PTR
#include "Demo_MemMap.h"

#define DEMO_START_SEC_VAR_FAST_CLEARED_UNSPECIFIED
#include "Demo_MemMap.h"
    DemoUnspecifiedTpye DemoVarFastClearedUnspecified = {0, 0, 0};
#define DEMO_STOP_SEC_VAR_FAST_CLEARED_UNSPECIFIED
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_BOOLEAN
#include "Demo_MemMap.h"
    const boolean DemoConstVarBool[] = {TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE};
#define DEMO_STOP_SEC_CONST_BOOLEAN
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_8
#include "Demo_MemMap.h"
    const uint8 DemoConstVar8[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_CONST_8
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_16
#include "Demo_MemMap.h"
    const uint16 DemoConstVar16[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_CONST_16
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_32
#include "Demo_MemMap.h"
    const uint32 DemoConstVar32[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_CONST_32
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_PTR
#include "Demo_MemMap.h"
    const uint8 * const DemoConstVarPtr[] = {(uint8 *)0x1000};
#define DEMO_STOP_SEC_CONST_PTR
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_UNSPECIFIED
#include "Demo_MemMap.h"
    const DemoUnspecifiedTpye DemoConstVarUnspecified = {1, 2, 3};
#define DEMO_STOP_SEC_CONST_UNSPECIFIED
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_FAST_BOOLEAN
#include "Demo_MemMap.h"
    const boolean DemoConstFastVarBool[] = {TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE};
#define DEMO_STOP_SEC_CONST_FAST_BOOLEAN
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_FAST_8
#include "Demo_MemMap.h"
    const uint8 DemoConstFastVar8[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_CONST_FAST_8
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_FAST_16
#include "Demo_MemMap.h"
    const uint16 DemoConstFastVar16[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_CONST_FAST_16
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_FAST_32
#include "Demo_MemMap.h"
    const uint32 DemoConstFastVar32[] = {1, 2, 3, 4, 5, 6};
#define DEMO_STOP_SEC_CONST_FAST_32
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_FAST_PTR
#include "Demo_MemMap.h"
    const uint8 * const DemoConstFastVarPtr[] = {(uint8 *)0x1000};
#define DEMO_STOP_SEC_CONST_FAST_PTR
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CONST_FAST_UNSPECIFIED
#include "Demo_MemMap.h"
    const DemoUnspecifiedTpye DemoConstFastVarUnspecified = {1, 2, 3};
#define DEMO_STOP_SEC_CONST_FAST_UNSPECIFIED
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CODE_FAST
#include "Demo_MemMap.h"

    void func_code_fast()
    {
        printf("%s [addr=0x%08X]\r\n", __func__, (uint32)&func_code_fast);

        TEST_ARR(DemoVarFastInitBool);
        TEST_ARR(DemoVarFastInit8);
        TEST_ARR(DemoVarFastInit16);
        TEST_ARR(DemoVarFastInit32);
        TEST_ARR(DemoVarFastInitPtr);
        TEST_STRUCT(DemoVarFastInitUnspecified, member_a);
        TEST_ARR(DemoVarFastClearedBool);
        TEST_ARR(DemoVarFastCleared8);
        TEST_ARR(DemoVarFastCleared16);
        TEST_ARR(DemoVarFastCleared32);
        TEST_ARR(DemoVarFastClearedPtr);
        TEST_STRUCT(DemoVarFastClearedUnspecified, member_a);
        printf("\r\n");
    }

#define DEMO_STOP_SEC_CODE_FAST
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CODE
#include "Demo_MemMap.h"

    void func_code_normal()
    {
        printf("%s [addr=0x%08X]\r\n", __func__, (uint32)&func_code_normal);

        TEST_ARR(DemoVarInitBool);
        TEST_ARR(DemoVarInit8);
        TEST_ARR(DemoVarInit16);
        TEST_ARR(DemoVarInit32);
        TEST_ARR(DemoVarInitPtr);
        TEST_STRUCT(DemoVarInitUnspecified, member_a);
        TEST_ARR(DemoVarClearedBool);
        TEST_ARR(DemoVarCleared8);
        TEST_ARR(DemoVarCleared16);
        TEST_ARR(DemoVarCleared32);
        TEST_ARR(DemoVarClearedPtr);
        TEST_STRUCT(DemoVarClearedUnspecified, member_a);
        printf("\r\n");
    }

#define DEMO_STOP_SEC_CODE
#include "Demo_MemMap.h"

#define DEMO_START_SEC_CODE_SLOW
#include "Demo_MemMap.h"

void func_code_slow()
{
    printf("%s [addr=0x%08X]\r\n", __func__, (uint32)&func_code_slow);

    TEST_ARR(DemoConstVarBool);
    TEST_ARR(DemoConstVar8);
    TEST_ARR(DemoConstVar16);
    TEST_ARR(DemoConstVar32);
    TEST_ARR(DemoConstVarPtr);
    TEST_STRUCT(DemoConstVarUnspecified, member_a);
    TEST_ARR(DemoConstFastVarBool);
    TEST_ARR(DemoConstFastVar8);
    TEST_ARR(DemoConstFastVar16);
    TEST_ARR(DemoConstFastVar32);
    TEST_ARR(DemoConstFastVarPtr);
    TEST_STRUCT(DemoConstFastVarUnspecified, member_a);

    TEST_ARR(DemoCfgBool);
    TEST_ARR(DemoCfg8);
    TEST_ARR(DemoCfg16);
    TEST_ARR(DemoCfg32);
    TEST_ARR(DemoCfgPtr);
    TEST_STRUCT(DemoCfgUnspecified, member_a);
    printf("\r\n");
}

#define DEMO_STOP_SEC_CODE_SLOW
#include "Demo_MemMap.h"

#ifdef __cplusplus
}
#endif /* __cplusplus */
