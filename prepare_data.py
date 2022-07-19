def prepare_data_for_ai(self):
    train_input_df, train_target_df, all_train_labels = self.processing.serve_train_data()
    # prepare a numpy array contains copies of input and output based on window size.(prepare for AI)
    window_input = self.params["InputWindowSize"]
    # TODO: get following value from params later.
    # window_output = self.params["OutputWindowSize"]
    window_output = self.processing.get_output_window_size()
    # cut initial part of target to have same size as train.(prepare for AI)
    # _train_target_df = train_target_df.iloc[window_input:]

    # _train_target_df = ProcessingUtils.deform_based_on_window_size(df=train_target_df.iloc[window_input:],
    #                                                                window=window_output)
    _train_target_df = train_target_df.iloc[window_input - 1:].to_numpy()

    train_input = ProcessingUtils.deform_based_on_window_size(df=train_input_df, window=window_input)
    # reshape data from three dimensional array to two dimensional array to be feed into
    # imbalanced method
    # check if training is three dimensional or not
    input_shape = train_input.shape
    if len(input_shape) == 3:

        input_imbalance = train_input.reshape(input_shape[0], -1)
    else:
        input_imbalance = train_input
    if len(_train_target_df.shape) > 2:
        raise ValueError("Imbalanced method for target dimension greater than one is not availabe")
    else:
        target_imbalance = _train_target_df
    # Apply imbalance method
    # convert numpy arrays to dataframe
    all_train_labels_reshape = all_train_labels.copy()
    train_labels_reshape_temp = all_train_labels.copy()
    for i in range(1, window_input):
        for j in range(0, len(all_train_labels)):
            train_labels_reshape_temp[j] = str(all_train_labels[j]) + '_' + str(i)
        all_train_labels_reshape = all_train_labels_reshape + train_labels_reshape_temp
    target_columns = self.curve_details['Target']['property'].get('Child', None)
    if target_columns is None:
        target_columns = ['Target']
    target_imbalance_df = pd.DataFrame(columns=target_columns, data=target_imbalance)
    input_imbalance_df = pd.DataFrame(columns=all_train_labels_reshape, data=input_imbalance)
    so_train_input, so_train_target = QRImbalancedSampling.main(self.curve_details,
                                                                train_data=input_imbalance_df,
                                                                target_data=target_imbalance_df)
    # Return shape of data to three dimensional. Imbalance change first dimension
    if len(input_shape) == 3:
        final_train_input = so_train_input.to_numpy().reshape(-1, input_shape[1], input_shape[2])
        final_train_target = so_train_target.to_numpy()
    else:
        final_train_input = so_train_input.to_numpy()
        final_train_target = so_train_target.to_numpy()

    return final_train_input, final_train_target, all_train_labels



def deform_based_on_window_size(cls, df, window, **kwargs):
    train_data = df.to_numpy()
    if window > 1:
        condition = len(train_data.shape) > 1
        if condition:
            m, n = train_data.shape
            s0, s1 = train_data.strides
            _shape = (m - window + 1, window, n)
            _strides = (s0, s0, s1)
        else:
            m, n = (train_data.shape[0], None)
            s0, s1 = (train_data.strides[0], None)
            _shape = (m - window + 1, window)
            _strides = (s0, s0)

        return np.lib.stride_tricks.as_strided(train_data, shape=_shape, strides=_strides)
    return train_data

