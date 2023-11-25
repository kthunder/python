module_list = [
    # "Demo",
    "Adc",
    "Base",
    "Can",
    "Crc",
    "Crypto",
    "Dio",
    "Dma",
    "Eep",
    "Eth",
    "Fls",
    "Ftm",
    "Gpt",
    "Gtm",
    "I2c",
    "I3c",
    "Icu",
    "Lin",
    "Mcal",
    "Mcl",
    "Mcu",
    "Ocu",
    "Platform",
    "Port",
    "Pwm",
    "Sai",
    "Sent",
    "Spi",
    "Stm",
    "Uart",
    "Wdg",
]

module_list_safety = [
    "AdcSensor",
    "Eim",
    "Endinit",
    "Intm",
    "Iom",
    "SafetyMtl",
    "Smu",
    "Stcu"
]

FILE_TEMPLATE = """
/************************************************************************************
*  Copyright (c) 2023, ThinkTech, Inc. All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without modification,
*  are permitted provided that the following conditions are met:
*
*  1) Redistributions of source code must retain the above copyright notice, this
*     list of conditions and the following disclaimer.
*
*  2) Redistributions in binary form must reproduce the above copyright notice, this
*     list of conditions and the following disclaimer in the documentation and/or
*     other materials provided with the distribution.
*
*  3) Neither the name of the ThinkTech, Inc., nor the names of its contributors may
*     be used to endorse or promote products derived from this software without
*     specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
*  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
*  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
*  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
*  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
*  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
*  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
*  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
*  OF THE POSSIBILITY OF SUCH DAMAGE.
*************************************************************************************/
#ifdef __cplusplus
extern "C"{{
#endif

#define {mdl_upper}_MEMMAP_VENDOR_ID_H                    1541
#define {mdl_upper}_MEMMAP_AR_RELEASE_MAJOR_VERSION_H     4
#define {mdl_upper}_MEMMAP_AR_RELEASE_MINOR_VERSION_H     4
#define {mdl_upper}_MEMMAP_AR_RELEASE_PATCH_VERSION_H     0
#define {mdl_upper}_MEMMAP_SW_MAJOR_VERSION_H             1
#define {mdl_upper}_MEMMAP_SW_MINOR_VERSION_H             0
#define {mdl_upper}_MEMMAP_SW_PATCH_VERSION_H             0

/**
* @brief Symbol used for checking correctness of the includes
*/
#define MEMMAP_ERROR


#if defined (_HITECH_C_ALIOTHXX_) || (_LLVM_C_ALIOTHXX_)

{hightec_patch}
#else /* TODO: Check arm-none-eabi-gcc, assume gcc */

{gcc_patch}
#endif /* compile end */

#ifdef __cplusplus
}}
#endif

"""

TEMPLATE_HIGHTEC_PATCH = """\
#ifdef {mdl_upper}_START_SEC_{key}
    /**
    * @file {mdl}_MemMap.h
    * @violates @ref {mdl}_MemMap.h_MemMap_h_REF_1 MISRA 2012 Required Rule 19.6, use of '#undef' is discouraged
    */
    #undef {mdl_upper}_START_SEC_{key}
    #define ENTERED_{mdl_upper}_START_SEC_{key}
    #ifndef MEMMAP_MATCH_ERROR
       #define MEMMAP_MATCH_ERROR
    #else
        #ifndef {mdl_upper}_STOP_SEC_{key}
        #error "MemMap.h, no valid matching start-stop section defined."
        #endif
    #endif
    /**
    * @file {mdl}_MemMap.h
    * @violates @ref {mdl}_MemMap.h_REF_1 MISRA 2012 Required Rule 19.6, use of '#undef' is discouraged
    */
    #undef MEMMAP_ERROR
    #pragma clang section {mod_line}
#endif
#ifdef {mdl_upper}_STOP_SEC_{key}
    /**
    * @file {mdl}_MemMap.h
    * @violates @ref {mdl}_MemMap.h_MemMap_h_REF_1 MISRA 2012 Required Rule 19.6, use of '#undef' is discouraged
    */
    #ifdef ENTERED_{mdl_upper}_START_SEC_{key}
        #undef ENTERED_{mdl_upper}_START_SEC_{key}
    #else
        #error "MemMap.h, no valid matching start-stop section defined."
    #endif
    #ifdef MEMMAP_MATCH_ERROR
        #undef MEMMAP_MATCH_ERROR
    #endif
    #undef {mdl_upper}_STOP_SEC_{key}
    /**
    * @file {mdl}_MemMap.h
    * @violates @ref {mdl}_MemMap.h_REF_1 MISRA 2012 Required Rule 19.6, use of '#undef' is discouraged
    */
    #undef MEMMAP_ERROR
    #pragma clang section bss="" data="" rodata="" text=""
#endif

"""

TEMPLATE_GCC_PATCH = """\
#ifdef {mdl_upper}_START_SEC_{key}
    #undef {mdl_upper}_START_SEC_{key}
#endif
#ifdef {mdl_upper}_STOP_SEC_{key}
    #undef {mdl_upper}_STOP_SEC_{key}
#endif

"""


def gen_memmap_file(module_name, gen_path):
    with open(f'memmap_include_headers/{gen_path}/{module_name}_MemMap.h', 'w') as of:
        hightec_patch = ''
        gcc_patch = ''
        with open('MmeMapConfig.csv') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                key, sec_name, sec = line.split(',')
                key = key.strip()
                sec_name = sec_name.strip()
                sec = sec.strip()
                mod_section = dict(bss="", data="", rodata="", text="")
                mod_section[sec_name] = sec + f".{module_name.lower()}"
                mod_line = ' '.join(f'{k}="{v}"' for k, v in mod_section.items())
                
                hightec_patch += TEMPLATE_HIGHTEC_PATCH.format(
                    mdl=module_name,
                    mdl_upper=module_name.upper(),
                    key=key,
                    mod_line=mod_line,
                )
                gcc_patch += TEMPLATE_GCC_PATCH.format(
                    mdl=module_name,
                    mdl_upper=module_name.upper(),
                    key=key,
                    mod_line=mod_line,
                )
        of.write(FILE_TEMPLATE.format(
            mdl=module_name,
            mdl_upper=module_name.upper(),
            hightec_patch=hightec_patch,
            gcc_patch=gcc_patch,
        ))


if __name__ == '__main__':
    for module in module_list:
        gen_memmap_file(module, 'memmap_inc')
    for module in module_list_safety:
        gen_memmap_file(module, 'memmap_inc_safety')
