from iocx.readers.vdif.tools.vdif_generator import generate_vdif

# Enable for generating 1/1000 of the test data
SUB_TEST = True
# TODO: se proper configuration in media.ini (fs)


if SUB_TEST:
    fs = 2e7
    Bpf = 1000
    seconds_duration = 2
    prefix = "./examples/test_dataset_test/sub/media/new_"
else:
    fs = 2e9
    Bpf = 100000
    seconds_duration = 20
    prefix = "./examples/test_dataset_test/full/media/new_"
date = [2015, 11, 24, 18, 57, 35]
bps=2
log_2_channels = 1
complex = False

bw = fs
if not complex:
    bw = fs/2
bw = bw*(2**log_2_channels)

generate_vdif(tot_stations=1,
              bw_in=bw,
              bytes_payload_per_frame=Bpf,
              bits_quant=bps, #4,
              snr_in=1e2,
              sines_f_in=[],
              sines_amp_in=[], \
              prefix="test_s",
              signal_limits=[0, 0],
              log_2_channels=log_2_channels,
              num_threads=1,
              threaded_channels=0,
              num_taps_filterbank=256, \
              date_vector=date,
              seconds_duration=seconds_duration,
              v=0,
              force_complex=complex,
              data_dir=prefix,
              )
