/*******************************************************************************
**                                                                            **
** Copyright (C) ThinkTech Technologies (2023)                                **
**                                                                            **
** All rights reserved.                                                       **
**                                                                            **
** This document contains proprietary information belonging to ThinkTech      **
** Technologies. Passing on and copying of this document, and communication   **
** of its contents is not permitted without prior written authorization.      **
**                                                                            **
********************************************************************************
**                                                                            **
**  FILENAME     :linker_flash_A8V2.ld                                          **
**                                                                            **
**  VERSION      : 1.0.0                                                      **
**                                                                            **
**  PLATFORM     : ThinkTech Alioth Series                                    **
**                                                                            **
**  VENDOR       : ThinkTech Technologies                                     **
**                                                                            **
**  DESCRIPTION  : Base Driver Source File                                     **
**                                                                            **
**  MAY BE CHANGED BY USER : yes                                              **
**                                                                            **
*******************************************************************************/
HEAP_SIZE  = DEFINED(__heap_size__)  ? __heap_size__  : 0x00002000;
RENTATION_SIZE = 0x8000;

ENTRY(Reset_IRQHandler)

MEMORY 
{         
    int_flash               : ORIGIN = 0x01000000, LENGTH = 0x00400000    /* 4MB */
    int_dflash              : ORIGIN = 0x01500000, LENGTH = 0x00040000    /* 256K */
    int_itcm                : ORIGIN = 0x00000000, LENGTH = 0x00008000    /* 32K */
    int_dtcm                : ORIGIN = 0x20000000, LENGTH = 0x00040000    /* 256K */
    int_sram                : ORIGIN = 0x20100000, LENGTH = 0x00038000    /* 224K */
    int_sram_stack_c        : ORIGIN = 0x20138000, LENGTH = 0x00004000    /* 16KB  */
    int_sram_no_cacheable   : ORIGIN = 0x2013C000, LENGTH = 0x00004000    /* 16KB  */
    ram_end                 : ORIGIN = 0x20140000, LENGTH = 0             /* End of SRAM */
}

SECTIONS
{
    /* text sections, store in PFlash */
    .text :
    {
        __text_start = .;
        __interrupts_rom_start = .;
        KEEP(*(.intc_vector))    
        . = ALIGN(4); 
        __interrupts_rom_end = .;
        . = ALIGN(4);
        *(.startup) 
        . = ALIGN(4);
        *(.systeminit) 
        . = ALIGN(4);
        *(.text.startup) 
        . = ALIGN(4);
        *(.text)
        *(.text*) 
        
        /* MODIFIED HERE */
        . = ALIGN(4);
        *(.mcal_text_normal.*)
        . = ALIGN(4);
        *(.mcal_text_slow.*)
        . = ALIGN(4);
        *(.mcal_config_data_unspecified.*)
        
        . = ALIGN(4);
        *(.mcal_text) 
        . = ALIGN(4);
        *(.saf_text) 
        . = ALIGN(4);
        *(.acmcu_code_rom)
        . = ALIGN(4);
        KEEP(*(.init))
        . = ALIGN(4);
        KEEP(*(.fini)) 
       
        . = ALIGN(4);
        *(.rodata)  
        *(.rodata*)  
        . = ALIGN(4);
        *(.mcal_const_cfg)  
        . = ALIGN(4);
        *(.mcal_const)  
        . = ALIGN(4);
        *(.saf_const_cfg)  
        . = ALIGN(4);
        *(.saf_const)  
         . = ALIGN(32);
    } > int_flash
    
    .ARM.extab   : { 
        *(.ARM.extab* .gnu.linkonce.armextab.*) 
    } >int_flash
    
    .ARM : {
        __exidx_start = .;
        *(.ARM.exidx*)
        __exidx_end = .;
    } >int_flash
  
    .preinit_array     :
    {
        PROVIDE_HIDDEN (__preinit_array_start = .);
        KEEP (*(.preinit_array*))
        PROVIDE_HIDDEN (__preinit_array_end = .);
    } >int_flash
    
    .init_array :
    {
        PROVIDE_HIDDEN (__init_array_start = .);
        KEEP (*(SORT(.init_array.*)))
        KEEP (*(.init_array*))
        PROVIDE_HIDDEN (__init_array_end = .);
    } >int_flash
  
    .fini_array :
    {
        PROVIDE_HIDDEN (__fini_array_start = .);
        KEEP (*(SORT(.fini_array.*)))
        KEEP (*(.fini_array*))
        PROVIDE_HIDDEN (__fini_array_end = .);
    } >int_flash
    
    .tt_table :{
        . = ALIGN(4);
        __tt_init_table = .;
        KEEP(*(.tt_init_table))    /* store init_table address */
        . = ALIGN(4);
        __tt_zero_table = .;
        KEEP(*(.tt_zero_table)) /* store zero_table address */
    } >int_flash
     . = ALIGN(16);
    __text_end = .;
    __sram_data_rom = __text_end;
/* ================ flash text end ================================= */
     .sram_data : AT(__sram_data_rom)
    {
        . = ALIGN(4);
        __sram_data_begin__ = .; 
        __retention_sram_begin__ = .; 
        *(.rentationRam);
        __retention_sram_end__ = .; 
        . = ALIGN(4);
        *(.ramcode)    
        . = ALIGN(4);
        *(.data)  
        *(.data*)
        . = ALIGN(4);
        *(.mcal_data)
        . = ALIGN(4);
        *(.saf_data)
        . = ALIGN(4);
        _GOT_START_ = ABSOLUTE (.);
        *(.got)
        _GOT_END_ = ABSOLUTE (.);
           __sram_data_end__ = .;
    } > int_sram

    __sram_data_rom_end = __sram_data_rom + (__sram_data_end__ - __sram_data_begin__);
        
    .sram_bss (NOLOAD) :
    {
        . = ALIGN(16);
        __sram_bss_start = .;
        *(.bss)
        *(.bss*)
        . = ALIGN(16);
        
        /* MODIFIED HERE */
        *(.mcal_data_cleared_boolean.*)
        *(.mcal_data_cleared_16.*)
        *(.mcal_data_cleared_ptr.*)
        . = ALIGN(4);
        
        *(.mcal_bss)
        . = ALIGN(4);
        *(.saf_bss)
        . = ALIGN(4);
        __sram_bss_end = .;
    } >int_sram AT>int_sram

   /* User_heap_stack section, used to check that there is enough RAM left */
    .heap (NOLOAD):
    {
        . = ALIGN(8);
        PROVIDE ( end = . );
        PROVIDE ( _end = . );
        PROVIDE ( _heap_start = . );
        PROVIDE ( __HEAP = . );
        . = . + HEAP_SIZE;
        PROVIDE ( _heap_end = . );
        PROVIDE ( _Heap_Limit = . );
    } >int_sram AT>int_sram

    __non_cacheable_data_rom = __sram_data_rom_end;

    .non_cacheable_data : AT(__non_cacheable_data_rom)
    {
        . = ALIGN(4);
        __non_cacheable_data_start__ = .;
        . = ALIGN(4096);
        __interrupts_ram_start = .;
        . += __interrupts_rom_end - __interrupts_rom_start;    
        . = ALIGN(4);
        __interrupts_ram_end = .;
        *(.mcal_data_no_cacheable)        
        . = ALIGN(4);
        *(.mcal_const_no_cacheable)      
        . = ALIGN(4);
        *(.saf_data_no_cacheable)        
        . = ALIGN(4);
        *(.saf_const_no_cacheable)      
        . = ALIGN(4);
        HSE_LOOP_ADDR = .;
        LONG(0x0);
        __non_cacheable_data_end__ = .;  
    } > int_sram_no_cacheable
         
    __non_cacheable_data_rom_end = __non_cacheable_data_rom + (__non_cacheable_data_end__ - __non_cacheable_data_start__);
    .non_cacheable_bss (NOLOAD) :
    {  
        . = ALIGN(16);
        __non_cacheable_bss_start = .;
        *(.mcal_bss_no_cacheable)      
        . = ALIGN(4);
        *(.saf_bss_no_cacheable)      
        . = ALIGN(4);
        __non_cacheable_bss_end = .;       
    } >int_sram_no_cacheable AT>int_sram_no_cacheable
       
    __itcm_text_rom_start = __non_cacheable_data_rom_end ;
    
    .itcm_text : AT(__itcm_text_rom_start)
    {
        . = ALIGN(4);
        __itcm_text_ram_start__ = .;
        *(.mcal_text_itcm)        
        . = ALIGN(4);
        
        /* MODIFIED HERE */
        *(.mcal_text_fast.*)
        . = ALIGN(4);
        
        *(.saf_text_itcm)        
        __itcm_text_ram_end__ = .;  
    } > int_itcm
    
    __itcm_text_rom_end = __itcm_text_rom_start + (__itcm_text_ram_end__ - __itcm_text_ram_start__) ;
    __dtcm_data_rom_start = __itcm_text_rom_end ;
    
    .dtcm_data : AT(__dtcm_data_rom_start)
    {
        . = ALIGN(4);
        __dtcm_data_ram_start__ = .;
          
        *(.mcal_data_dtcm)        
        . = ALIGN(4);
        *(.saf_data_dtcm)        
        __dtcm_data_ram_end__ = .;  
    } > int_dtcm 
    
    __dtcm_data_rom_end = __dtcm_data_rom_start + (__dtcm_data_ram_end__ - __dtcm_data_ram_start__) ;
    
    .dtcm_bss (NOLOAD) :
    {
        . = ALIGN(16);
        __dtcm_bss_start = .;
        
        /* MODIFIED HERE */
        . = ALIGN(4);
        *(.mcal_data_fast_cleared_16.*)
        . = ALIGN(4);
        *(.mcal_data_fast_cleared_unspecified.*)
          
        *(.mcal_bss_dtcm)
        . = ALIGN(4);
        
        *(.saf_bss_dtcm)
        . = ALIGN(4);
        __dtcm_bss_end = .;
    } >int_dtcm AT>int_dtcm
        
    __Stack_end_c           = ORIGIN(int_sram_stack_c);
    __Stack_start_c         = ORIGIN(int_sram_stack_c) + LENGTH(int_sram_stack_c);

    __INT_SRAM_START         = ORIGIN(int_sram);
    __INT_SRAM_END           = ORIGIN(ram_end);
    
    __INT_ITCM_START         = ORIGIN(int_itcm);
    __INT_ITCM_END           = ORIGIN(int_itcm) + LENGTH(int_itcm);
    
    __INT_DTCM_START         = ORIGIN(int_dtcm);
    __INT_DTCM_END           = ORIGIN(int_dtcm) + LENGTH(int_dtcm);
        
    __RAM_NO_CACHEABLE_START = ORIGIN(int_sram_no_cacheable);
    __RAM_NO_CACHEABLE_END   = ORIGIN(int_sram_no_cacheable) + LENGTH(int_sram_no_cacheable);
    __RAM_NO_CACHEABLE_SIZE  = 0x0D;  /* 16kbyte*/
    __ROM_NO_CACHEABLE_START = __non_cacheable_data_rom;
    __ROM_NO_CACHEABLE_END   = __non_cacheable_data_rom_end;
    
    __RAM_CACHEABLE_START    = ORIGIN(int_sram);
    __RAM_CACHEABLE_END      = ORIGIN(int_sram_no_cacheable)-1;
    __RAM_CACHEABLE_SIZE     = 0x12; 
    __ROM_CACHEABLE_START    = __sram_data_rom;
    __ROM_CACHEABLE_END      = __sram_data_rom_end;

    __RAM_ITCM_START         = ORIGIN(int_itcm); 
    __RAM_ITCM_END           = ORIGIN(int_itcm) + LENGTH(int_itcm);
    __RAM_ITCM_SIZE          = 0x10;  
    __ROM_ITCM_START         = __itcm_text_rom_start;
    __ROM_ITCM_END           = __itcm_text_rom_end;
    
    __RAM_DTCM_START         = ORIGIN(int_dtcm);
    __RAM_DTCM_END           = ORIGIN(int_dtcm) + LENGTH(int_dtcm);
    __RAM_DTCM_SIZE          = 0x10;  
    __ROM_DTCM_START         = __dtcm_data_rom_start;
    __ROM_DTCM_END           = __dtcm_data_rom_end;
    
    __ROM_CODE_START         = ORIGIN(int_flash);
    __ROM_DATA_START         = ORIGIN(int_dflash); /* DFlash */
    
    
    __BSS_SRAM_START         = __sram_bss_start;
    __BSS_SRAM_END           = __sram_bss_end;
    __BSS_SRAM_SIZE          = __sram_bss_end - __sram_bss_start;
    
    __BSS_SRAM_NC_START      = __non_cacheable_bss_start;
    __BSS_SRAM_NC_SIZE       = __non_cacheable_bss_end - __non_cacheable_bss_start;
    __BSS_SRAM_NC_END        = __non_cacheable_bss_end;

    __RAM_INTERRUPT_START    = __interrupts_ram_start;
    __ROM_INTERRUPT_START    = __interrupts_rom_start;
    __ROM_INTERRUPT_END      = __interrupts_rom_end;

    __BSS_DTCM_START         = __dtcm_bss_start;
    __BSS_DTCM_END           = __dtcm_bss_end;
    __BSS_DTCM_SIZE          = __sram_bss_end - __sram_bss_start;

    __TT_INIT_TABLE             = __tt_init_table;
    __TT_ZERO_TABLE             = __tt_zero_table;
    
    __RAM_INIT               = 0;  /* Hw has aready init */
    __ITCM_INIT              = 1; /* if used itcm */
    __DTCM_INIT              = 1; /* if used dtcm */
    __RETENTION_SIZE		 = __retention_sram_end__ - __retention_sram_begin__;
         
    __ENTRY_VTABLE              = __ROM_INTERRUPT_START;
    
    __COREM7_VTOR             = __RAM_INTERRUPT_START;

}
