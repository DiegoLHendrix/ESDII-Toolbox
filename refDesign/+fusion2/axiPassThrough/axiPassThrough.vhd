-------------------------------------------------------------------------------
-- Dr. Kaputa
-- axiPassThrough 
-------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;      

entity axiPassThrough is
  port (
    aclk                      : in  std_logic;
    resetn                    : in  std_logic;
    m_axis_video_tdata        : in  std_logic_vector(63 downto 0); 
    m_axis_video_tlast        : in  std_logic;
    m_axis_video_tready       : out std_logic;
    m_axis_video_tuser        : in  std_logic;
    m_axis_video_tvalid       : in  std_logic;
    
    s_axis_video_tdata        : out std_logic_vector(63 downto 0); 
    s_axis_video_tlast        : out std_logic;
    s_axis_video_tready       : in std_logic;
    s_axis_video_tuser        : out std_logic;
    s_axis_video_tvalid       : out std_logic
  );  
end axiPassThrough;  

architecture beh of axiPassThrough  is

begin
  s_axis_video_tdata      <= m_axis_video_tdata; 
  s_axis_video_tlast      <= m_axis_video_tlast; 
  m_axis_video_tready     <= s_axis_video_tready;
  s_axis_video_tuser      <= m_axis_video_tuser; 
  s_axis_video_tvalid     <= m_axis_video_tvalid;
end beh;